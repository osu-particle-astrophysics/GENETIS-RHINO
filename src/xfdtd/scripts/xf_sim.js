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
    App.getActiveProject().getMaterialList().deleteMaterial(pec.name);
  }
  App.getActiveProject().getMaterialList().addMaterial(pec);
}

// Make the grid spacing (or "resolution")
function create_grid(setup_data) {
  var x = setup_data.x;
  var y = setup_data.y;
  var d = setup_data.d;
  // Set up the grid spacing for the antenna
  var grid = App.getActiveProject().getGrid();
  var cellSizes = grid.getCellSizesSpecification();

  cellSizes.setTargetSizes(Cartesian3D(3, 3, 3));
  // And we need to set the Minimum Sizes - these are the minimum deltas that we will allow in this project.
  // We'll use the scalar ratio of 20% here.
  cellSizes.setMinimumSizes(Cartesian3D("3", "3", "3"));
  cellSizes.setMinimumIsRatioX(true);
  cellSizes.setMinimumIsRatioY(true);
  cellSizes.setMinimumIsRatioZ(true);

  grid.specifyPaddingExtent(
    Cartesian3D("20", "20", "20"),
    Cartesian3D("20", "20", "20"),
    true,
    true
  );

  a = Math.sqrt(2 * (x - y));
  var boundingBox = new BoundingBox3D(
    new Cartesian3D("-" + x + "", "-" + x + "", "-" + d + ""),
    new Cartesian3D("" + x + " ", "" + x + " ", "0.05 ")
  );
  var cellSizeSpec = new CellSizesSpecification();
  cellSizeSpec.setTargetSizes(new Cartesian3D("0.9 mm", "0.9 mm", "0.9 mm"));
  cellSizeSpec.setMinimumSizes(new Cartesian3D("0.3 mm", "0.3 mm", "0.3 mm"));
  //	cellSizeSpec.setTargetSizes( new Cartesian3D(  "3*"+a+" m", "3*"+a+" m", "3*"+a+" m" ) );
  //	cellSizeSpec.setMinimumSizes( new Cartesian3D( ""+a+" m", ""+a+" m", ""+a+" m" ) );
  //	grid.addManualGridRegion( Grid.X | Grid.Y | Grid.Z, boundingBox, cellSizeSpec );
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

  Output.println("Successfully created the simulation.");
  Output.println("Submitting simulation job for individual " + setup_data.indv);

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
