"""This files contains functions for calculating fitness values."""

import glob

import healpy as hp
import numpy as np
import numpy.typing as npt
import pylab as plt
from astropy import units as u
from astropy.coordinates import AltAz, EarthLocation, Galactic, SkyCoord
from astropy.time import Time
from astropy_healpix import HEALPix


def beam_correction_factor(beam_power_db : npt.ArrayLike,
                           beam_alt_deg : npt.ArrayLike,
                           beam_az_deg : npt.ArrayLike,
                           beam_freqs_MHz : npt.ArrayLike,
                           beam_ref_idx : int,
                           ref_map_path : str="src/assets/haslam408_dsds_Remazeilles2014.fits",
                           location : EarthLocation = None,
                           obstime : Time = None) -> npt.ArrayLike:
    """
    Calculates the beam correction factor as defined in Eq. 7 of Spinelli et al. (2022) [https://doi.org/10.1093/mnras/stac1804].

    This factor accounts for the chromaticity of the beam as it couples
    to the radio foreground brightness temperature distribution. The
    measured frequency spectrum (antenna pattern times sky brightness,
    integrated over the sky at each frequency) can be divided by this
    factor to give a partial correction for the chromatic response of
    the beam.

    This function loads a reference temperature map, which is the Haslam
    all-sky 408 MHz map, reprocessed by Remazeilles et al. (2015). The
    reference frequency for the map is 408 MHz, and a simple power-law
    spectral index of beta = -2.7 is assumed.

    Args:
        beam_power_db (array_like):
            A 2D array containing the beam power pattern in dB as a function
            of frequency. This should not be peak-normalised. The shape
            should be `(Nfreqs, Npixels)`.
        beam_alt_deg (array_like):
            A 1D array containing the altitude coordinate of each element of
            `beam_power_db`, in degrees. The pattern is assumed to be
            pointing up at zenith, i.e. the boresight points to alt=90 deg.
        beam_az_deg (array_like):
            A 1D array containing the azimuth coordinate of each element of
            `beam_power_db`, in degrees
        beam_freqs_MHz (array_like):
            Frequencies that the beam correction factor should be evaluated at,
            in MHz.
        beam_ref_idx (int):
            Which reference frequency to use from the `beam_freqs_MHz` array.
        ref_map_path (str):
            Path to the Haslam 408 MHz map, `haslam408_dsds_Remazeilles2014.fits`. This
            can be obtained from the following URL:
            `http://www.jb.man.ac.uk/research/cosmos/haslam_map/haslam408_dsds_Remazeilles2014.fits`
        location (astropy.EarthLocation):
            Object containing the location of the observer. If left unspecified,
            will default to Jodrell Bank, `lat=53.2421deg, lon=-2.3067deg, flare_height=70`.
        obstime (astropy.Time):
            Object containing the time of the observation. If unspecified, will
            default to `2025-08-01 22:00:00Z`.

    Returns:
        bcf (array_like):
            Beam correction factor at each frequency. This is a dimensionless ratio.

    """
    # Load healpix reference map, assumed to be at 408 MHz
    spectral_index_ref_freq = 408. # MHz
    beta = -2.7 # spectral index for reference map power-law frequency spectrum
    ref_map = hp.fitsfunc.read_map(ref_map_path) # load map from fits file

    # Set up HP object, which is assuemd to be in Galactic coords
    hp_map = HEALPix(nside=hp.npix2nside(ref_map.size), order="RING", frame=Galactic())

    # Define local alt/az coordinate system
    if location is None:
        location = EarthLocation(lat=53.2421*u.deg, lon=-2.3067*u.deg, height=70.)
    if obstime is None:
        obstime = Time("2025-08-01 22:00:00Z")
    frame_altaz = AltAz(obstime=obstime, location=location)

    # Set up Astropy coordinate objects for each pixel of the beam
    coords = SkyCoord(beam_az_deg.ravel() * u.deg, beam_alt_deg.ravel() * u.deg, frame=frame_altaz)

    # Interpolate values of reference map onto the same coords as the beam
    tmap = hp_map.interpolate_bilinear_skycoord(coords, ref_map)

    # Integrals of beam at ref. frequency
    # (integral of beam and sky times beam over solid angle at ref. freq.)
    # All integrals are just sums, assuming fixed pixel area (true for healpix).
    # No pixel area factor is used as they should cancel in the BCF ratio.
    beam_ref = (10.**(beam_power_db[beam_ref_idx]/10.)).flatten() # convert dB to linear gain
    tsky_ref = tmap * (beam_freqs_MHz[beam_ref_idx] / spectral_index_ref_freq)**beta
    beam_integ_ref = np.sum(beam_ref)
    sky_times_beam_integ_ref = np.sum(beam_ref * tsky_ref)

    # Loop over frequencies to calculate BCF
    bcf = np.zeros(beam_freqs_MHz.size)
    for i, freq in enumerate(beam_freqs_MHz):
        # Beam and sky maps at this frequency
        beam = (10.**(beam_power_db[i]/10.)).flatten()
        #tsky = tmap * (freq / spectral_index_ref_freq)**beta

        # Integral of beam and ref. sky times beam at this frequency
        beam_integ = np.sum(beam)
        sky_times_beam_integ = np.sum(beam * tsky_ref)

        # Populate BCF value in array
        bcf[i] = (sky_times_beam_integ / sky_times_beam_integ_ref) \
               * (beam_integ_ref / beam_integ)
    return bcf


def calculate_bcf_stats(freqs : npt.ArrayLike, bcf : npt.ArrayLike) -> dict:
    """
    Very simple summary statistics about the beam correction factor.

    Args:
        freqs (array_like):
            Frequencies at which the BCF was evaluated. Assumed to be in MHz.
        bcf (array_like):
            Array of BCF values.

    Returns:
        stats (dict):
            Dictionary of simple summary statistics:
            - max_abs_deriv: Phil's favorite. Maximum value of the derivative of the
                BCF in frequency. Higher absolute values imply that somewhere in the
                frequency range, there is a more rapid variation of the BCF with
                frequency (lower is better)
            - rms: root mean squared ms deviation of the BCF from 1. It will penalise
                anything that deviates from 1, even if that deviation has no frequency
                structure (lower is better).
            - swing: difference between the maximum and minimum of the BCF. Can
                be used to penalise large variations across the band,
                regardless of whether they look smooth in frequency (lower is better)

    """
    stats = {}

    # Calculate RMS value
    stats["rms"] = np.sqrt(np.mean((bcf - 1.)**2.))

    # Calculate swing
    stats["swing"] = bcf.max() - bcf.min()

    # Calculate max. absolute derivative
    # Lower is better
    stats["max_abs_deriv"] = np.max(np.abs(np.diff(bcf) / np.diff(freqs)))
    return stats


def load_uan(fname : str) -> tuple[float, npt.ArrayLike, npt.ArrayLike, npt.ArrayLike]:
    """Load antenna pattern data from a UAN text file."""
    def strip_header(f : str) -> tuple[int, int, str, float]:
        # Parse and strip header lines from input file
        phi_inc = theta_inc = magnitude = None    # need these to process the file
        line = f.readline()
        while "end_<parameters>" not in line:
            if "phi_inc" in line:
                phi_inc = int(line.split()[1])
            if "theta_inc" in line:
                theta_inc = int(line.split()[1])
            if "magnitude" in line:
                magnitude_unit = line.split()[1]
            if "frequencyHz" in line:
                freq_hz = float(line.split()[1])
            line = f.readline()

        # Check headers were found
        assert  phi_inc is not None \
            and theta_inc is not None \
            and magnitude_unit is not None \
            and freq_hz is not None, \
            "Required headers missing"
        return phi_inc, theta_inc, magnitude_unit, freq_hz

    def polar_to_re_im(fn : callable, amp : float, phase : float) -> complex:
        # amp in dB and phase in degrees
        return fn(amp) * (np.cos(np.deg2rad(phase)) + 1.j*np.sin(np.deg2rad(phase)))

    # Helper conversion functions
    def dB_to_lin(vals : npt.ArrayLike) -> npt.ArrayLike:
        return 10.**(vals/10.)

    def no_change(vals : npt.ArrayLike) -> npt.ArrayLike:
        return vals

    def to_power(efield : tuple[complex, complex]) -> float:
        return (efield[0] * np.conj(efield[0]) + efield[1] * np.conj(efield[1])).real

    # Open file and parse data
    with open(fname) as f:
        # Parse header
        za_inc, az_inc, magnitude_type, freq_hz = strip_header(f)

        # Load data from remaining rows in file
        uan_values = np.loadtxt(f)

    # Zenith angle and azimuth arrays
    za = np.sort(np.unique(uan_values[:, 0])).astype(int)
    az = np.sort(np.unique(uan_values[:, 1])).astype(int)

    # Rescaling function
    scale = no_change
    if magnitude_type == "dB":
        scale = dB_to_lin

    # Unpack antenna pattern values
    # (Naxes_vec, 1, Nfeeds or Npols, Nfreqs, Naxes2, Naxes1)
    values = np.zeros((za.size, az.size))
    for i in range(uan_values.shape[0]):
        _za = int(uan_values[i, 0])
        _az = int(uan_values[i, 1])

        # E-field as complex number
        E_za = polar_to_re_im(scale, uan_values[i, 2], uan_values[i, 4])
        E_az = polar_to_re_im(scale, uan_values[i, 3], uan_values[i, 5])
        assert values[_za//za_inc, _az//az_inc] == 0, \
               "az='%s' already has a value" % str(_az)

        # Convert E-field to power
        values[_za//za_inc, _az//az_inc] = to_power((E_az, E_za))

        # need to convert power to dB here
        # dB = 10 * log10(Watts / Reference Power)
        values[_za//za_inc, _az//az_inc] = 10 * np.log10(values[_za//za_inc, _az//az_inc])

    # Check that array isn't blank
    assert np.min(values) != 0
    return freq_hz, za, az, values


def load_uan_directory(path : str, suffix : str = ".uan") -> tuple[npt.ArrayLike, npt.ArrayLike, npt.ArrayLike, npt.ArrayLike]:
    """
    Load a series of UAN files from a directory, and pack into an array ordered by frequency.

    Args:
        path (str):
            Path to directory. This directory is assumed to contain a collection of uan
            files for the same antenna at different frequencies.
        suffix (str):
            Suffix of the data files, e.g. '.uan'.

    Returns:
        beams (array_like):
            Beams packaged together into shape `(Nfreqs, Nza, Naz)`.
        freqs (array_like):
            Frequency of each beam, in MHz.
        za (array_like):
            Zenith angle, in deg.
        az (array_like):
            Azimuth angle, in deg.

    """
    # Get list of files
    files = glob.glob("%s/*%s" % (path, suffix))

    # Current az, za arrays
    az, za = np.array([]), np.array([])

    # Loop over files
    freqs = []
    beam_list = []
    for fname in files:

        # Load file
        freq_hz, _za, _az, beam = load_uan(fname)

        # Compare az/za arrays to make sure the ordering is the same
        if az.size > 0:
            assert np.all(za == _za), "za arrays don't match"
            assert np.all(az == _az), "za arrays don't match"
        az = _az
        za  =_za

        # Store frequencies and beams
        freqs.append(freq_hz / 1e6) # convert to MHz
        beam_list.append(beam)

    # Re-order arrays
    idxs = np.argsort(freqs)
    beams = [beam_list[idx] for idx in idxs]
    beams = np.array(beams)
    freqs = np.unique(freqs)
    return beams, freqs, za, az


def calculate_fitnesses(uan_directory_root : str) -> dict:
    """
    Calculates fitness values (on all objectives).

    Args:
        uan_directory_root (str): Path to directory. This directory is assumed to
            contain a collection of uan files for the same antenna at
            different frequencies.

    Returns:
        bcf_statistics (dict): a dictionary where keys are statistic names and
            values are the values of those statistics (which can be used as fitness
            functions)

    """
    # freq_hz, za, az, values = load_uan("uan_files/0_uan_files/0/0_0_1.uan")

    # beams, freqs, za, az = load_uan_directory("uan_files/0_uan_files/1")
    beams, freqs, za, az = load_uan_directory(uan_directory_root)

    alt = 90-za              # Get altitude and work off that
    az_grid, alt_grid = np.meshgrid(az, alt)

    # beams = beams[:, :180, :360]

    print(beams.shape)

    # Calculate beam correction factor
    bcf = beam_correction_factor(beam_power_db=beams,
                                beam_alt_deg=alt_grid.flatten(),
                                beam_az_deg=az_grid.flatten(),
                                beam_freqs_MHz=freqs,
                                beam_ref_idx=freqs.size//2,
                                )

    return calculate_bcf_stats(freqs, bcf)


def make_plots(uan_directory_root : str) -> None:
    """
    Makes plots of the beam power and beam correction factor.

    Args:
        uan_directory_root (str): Path to directory. This directory is assumed to
            contain a collection of uan files for the same antenna at
            different frequencies.

    """
    beams, freqs, za, az = load_uan_directory(uan_directory_root)

    alt = 90-za              # Get altitude and work off that
    az_grid, alt_grid = np.meshgrid(az, alt)

    # beams = beams[:, :180, :360]

    print(beams.shape)

    # Calculate beam correction factor
    bcf = beam_correction_factor(beam_power_db=beams,
                                beam_alt_deg=alt_grid.flatten(),
                                beam_az_deg=az_grid.flatten(),
                                beam_freqs_MHz=freqs,
                                beam_ref_idx=freqs.size//2,
                                )

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.matshow(beams[0], vmax=20., vmin=-50., fignum=False, aspect="auto")
    cbar = plt.colorbar()
    plt.xlabel("Azimuth [deg]")
    plt.ylabel("Altitude [deg]")
    cbar.set_label("Beam power [dB]")

    plt.subplot(122)
    plt.plot(freqs, bcf)
    plt.xlabel("Freq. [MHz]")
    plt.ylabel("BCF")
    plt.tight_layout()
    plt.show()

