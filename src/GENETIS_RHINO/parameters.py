"""The parameters class store any config information we want to be able to easily modify via a toml file."""

try:
    from tomllib import load
except ModuleNotFoundError:
    from tomli import load

known_parameters = {
    "random_num_seed": int,
    "population_size": int,
    "num_generations": int,
    "per_site_mut_rate": float,
    "mut_effect_size": float,
    "selection_scheme": str,
    "percent_no_ridge_at_start": float,
    "NUM_WALL_PAIRS": int,
    "MIN_FLARE_LENGTH": float,
    "MAX_FLARE_LENGTH": float,
    "MIN_WAVEGUIDE_HEIGHT": float,
    "MAX_WAVEGUIDE_HEIGHT": float,
    "MIN_WAVEGUIDE_LENGTH": float,
    "MAX_WAVEGUIDE_LENGTH": float,
    "MIN_WAVEGUIDE_WIDTH": float,
    "MAX_WAVEGUIDE_WIDTH": float,
    "MIN_ANGLE": float,
    "MAX_ANGLE": float,
    "MIN_RIDGE_HEIGHT": float,
    "MAX_RIDGE_HEIGHT": float,
    "MIN_RIDGE_WIDTH_TOP": float,
    "MAX_RIDGE_WIDTH_TOP": float,
    "MIN_RIDGE_WIDTH_BOTTOM": float,
    "MAX_RIDGE_WIDTH_BOTTOM": float,
    "MIN_RIDGE_THICKNESS_TOP": float,
    "MAX_RIDGE_THICKNESS_TOP": float,
    "MIN_RIDGE_THICKNESS_BOTTOM": float,
    "MAX_RIDGE_THICKNESS_BOTTOM": float,
}

class ParametersObject:
    """This class serves as the interface for all parameters. Use ParametersObject.param_name to access a stored value."""

    def __init__(self, path_to_config: str) -> None:
        """Create a config object from a file."""
        with open(path_to_config, "rb") as f:
            self._parameters = load(f)

        print(f"{len(self._parameters)} parameters set by {path_to_config} .")

        # ensure all loaded values match a known parameter
        for name, value in self._parameters.items():
            # check name match
            if name not in known_parameters:
                raise KeyError(f"{name} is not a known parameter!")
            # check type match
            if not isinstance(value, known_parameters[name]):
                raise TypeError(f"Parameter {name} was loaded as type {type(value)}, but type {known_parameters[name]} was expected.")

        # check if all parameters have an assigned value.
        for param_name in known_parameters:
            if param_name not in self._parameters:
                raise ValueError(f"Parameter {param_name} not set!")


    def __getattr__(self, name: str) -> str:
        """Get a requested attribute."""
        _params = object.__getattribute__(self, "_parameters")
        if name not in _params:
            raise AttributeError(f"{name} is not a defined parameter!")
        return _params[name]
