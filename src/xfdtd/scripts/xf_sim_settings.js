// Functions related to setting up XFdtd simulation

// Creates the Perfect Electric Conductor material
function create_pec() {
  var pec = new Material();
  pec.name = "PEC";
  var pec_properties = new PEC();
  var pec_mag_freespace = new MagneticFreespace();
  var pec_phys_mat = new PhysicalMaterial();
  pec_phys_mat.setElectricProperties(pec_properties);
  pec_phys_mat.setMagneticProperties(pec_mag_freespace);
  pec.setDetails(pec_phys_mat);

  // Setting Color, historically white
  var pec_appearance = pec.getAppearance();
  var pec_face_appearance = pec_appearance.getFaceAppearance();
  pec_face_appearance.setColor(new Color(255, 255, 255, 255));

  // Check if material already exists
  if (null != App.getActiveProject().getMaterialList().getMaterial(pec.name)) {
    App.getActiveProject().getMaterialList().removeMaterial(pec.name);
  }
  App.getActiveProject().getMaterialList().addMaterial(pec);
}

// Make the grid spacing (or "resolution")
function create_grid(setup_data) {
  const unit_scale = setup_data.units === " cm" ? 0.01 : 1.0;
  const indvdata = setup_data.indvdata;
  const padding = "2"; // air buffer

  const horn_height =
    (indvdata.flare_height / 2) *
    MathUtils.evaluate(setup_data.num_wallpairs) *
    unit_scale;
  const half_width =
    (MathUtils.evaluate(indvdata.waveguide_width) / 2) * unit_scale;
  const half_length =
    (MathUtils.evaluate(indvdata.waveguide_length) / 2) * unit_scale;
  const wg_height = MathUtils.evaluate(indvdata.waveguide_height) / 2;

  const grid = App.getActiveProject().getGrid();

  // --- Air padding ---
  grid.specifyPaddingExtent(
    new Cartesian3D(padding, padding, padding),
    new Cartesian3D(padding, padding, padding),
    true,
    true
  );

  // --- Overall bounding box for horn + waveguide ---
  const fullBox = new BoundingBox3D(
    new Cartesian3D(-half_width, -half_length, -wg_height),
    new Cartesian3D(half_width, half_length, horn_height)
  );

  // --- Uniform cell settings ---
  const uniformCell = new CellSizesSpecification();
  uniformCell.setTargetSizes(new Cartesian3D("0.035 m", "0.035 m", "0.035 m"));
  uniformCell.setMinimumSizes(new Cartesian3D("0.017 m", "0.017 m", "0.017 m"));
  uniformCell.setMinimumIsRatioX(true);
  uniformCell.setMinimumIsRatioY(true);
  uniformCell.setMinimumIsRatioZ(true);

  grid.addManualGridRegion(Grid.X | Grid.Y | Grid.Z, fullBox, uniformCell);

  // --- Set boundary conditions directly on grid ---
  // X-axis
  grid.xLowerBoundaryType = "PMC"; // magnetic symmetry if geometry centered along x
  grid.xUpperBoundaryType = "Absorbing";

  // Y-axis
  grid.yLowerBoundaryType = "PMC"; // magnetic symmetry if geometry centered along y
  grid.yUpperBoundaryType = "Absorbing";

  // Z-axis (propagation)
  grid.zLowerBoundaryType = "Absorbing";
  grid.zUpperBoundaryType = "Absorbing";
  grid.absorptionType = "PML"; // PML absorbing boundary
  grid.numPMLLayers = "10";
}

// Make the sensors to detect the emitted signal
function create_sensors() {
  var sensor_data_def_list =
    App.getActiveProject().getSensorDataDefinitionList();
  sensor_data_def_list.clear();

  var far_sensor = new FarZoneSensor();
  far_sensor.retrieveSteadyStateData = true;
  far_sensor.setAngle1IncrementRadians(Math.PI / 36.0);
  far_sensor.setAngle2IncrementRadians(Math.PI / 36.0);
  far_sensor.name = "Far Zone Sensor";

  var far_zone_sensor_list = App.getActiveProject().getFarZoneSensorList();
  far_zone_sensor_list.clear();
  far_zone_sensor_list.addFarZoneSensor(far_sensor);
}

function create_sim_data(setup_data) {
  var sim_data = App.getActiveProject().getNewSimulationData();
  var FOI = sim_data.getFOIParameters();
  FOI.clearAllSpecifiedFrequencies();
  FOI.foiSource = 1;
  var freqs = setup_data.freqs;
  for (var k = 0; k < setup_data.num_freqs; k++) {
    FOI.addSpecifiedFrequency(freqs[k] + setup_data.freq_scale);
  }

  // Should already be done, but just in case
  sim_data.excitationType = NewSimulationData.DiscreteSources;
  if (setup_data.enable_sparams == false) {
    sim_data.enableSParameters = false;
  } else {
    sim_data.enableSParameters = true;
  }
}

// Queues Simulation to be ready for sim
function queue_sim(setup_data) {
  var simulation = App.getActiveProject().createSimulation(false);

  print("Successfully created the simulation.");
  print("Submitting simulation job for individual " + setup_data.indv);

  var project_id = simulation.getProjectId();
  var sim_id = simulation.getSimulationId();
  var num_runs = simulation.getRunCount();
}

// Takes image of antenna
function make_image(setup_data) {
  // Taking Picture of antenna on the side
  new_cam = Camera();
  new_cam.setPosition(Cartesian3D("0", "0", "15"));
  View.setCamera(new_cam);
  // Zooms out to include the entire detector, then saves as a .png
  View.zoomToExtents();
  var file = setup_data.indv_dir + "/side_image.png";
  View.saveImageToFile(file, -1, -1);

  // Taking picture at angle to the side and up a little
  new_cam2 = Camera();
  new_cam2.setPosition(Cartesian3D("10", "10", "10"));
  View.setCamera(new_cam2);
  View.zoomToExtents();
  var file = setup_data.indv_dir + "/1_1_angle_image.png";
  View.saveImageToFile(file, -1, -1);
}
