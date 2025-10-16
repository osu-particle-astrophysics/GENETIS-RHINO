// Persistent XFdtd implementation
var duration = 24 * 60 * 60 * 1000; // Time for while loop

// Persistent Function
main();

function main() {
  // Main function for persistent XFdtd
  var start_time = new Date().getTime();

  while (new Date().getTime() - start_time < duration) {
    var setup_dir = xf_run_scripts + "/setup";
    var output_dir = xf_run_scripts + "/output";

    // Check directory for setup file
    var setup_file = process_new_file(setup_dir);
    if (setup_file != null && setup_file != "") {
      var setup_data = jsonparse(setup_file);
      updateNextSimulationNumber(setup_data.indv);
      xf_setup(setup_data);
    }

    // Check diretory for output file
    var output_file = process_new_file(output_dir);
    if (output_file != null && output_file != "") {
      var output_data = jsonparse(output_file);

      xf_output(
        output_data.indv_dir,
        output_data.indv_num,
        output_data.num_freqs
      );
    }
  }
}

function xf_setup(setup_data) {
  // Function calls to setup xfdtd simulation and build antenna

  // Checking if simulation has already been done
  var sim_num = setup_data.indv;
  var simlength = sim_num.toString().length;
  var totchars = 6;
  var init = "";
  for (var i = 0; i < totchars - simlength; i++) {
    init = init + "0";
  }
  var sim_num = init + sim_num;
  var proj_dir = App.getActiveProject().getProjectDirectory();
  var sim_dir = new Dir(proj_dir + "/Simulations/" + sim_num + "/Run0001/");

  if (sim_dir.exists()) {
    return;
  } else {
    // Function calls for Antenna geometry building
    create_pec();
    // TODO: Add function call to build ridges
    build_waveguide(setup_data);
    build_horn(setup_data, setup_data.indvdata.wall_pair0);
    build_horn(setup_data, setup_data.indvdata.wall_pair1);
    create_feeds(setup_data);

    // Function calls for Simulation setup
    create_grid(setup_data);
    create_sensors(setup_data);
    create_sim_data(setup_data);
    queue_sim(setup_data);
    make_image(setup_data);

    clearLists(10000, 100);
  }
}

function jsonparse(fullpath) {
  var maxRetries = 50;
  var attempt = 0;

  while (attempt < maxRetries) {
    try {
      var file = new File(fullpath);
      file.open(1);
      var data = file.readAll();

      data = data.replace(/^\uFEFF/, "");

      var filedata = JSON.parse(data);
      file.close(1);
      return filedata;
    } catch (e) {
      print("Attempt " + (attempt + 1) + " failed: " + e);
      attempt++;
      App.sleep(100);
    }
  }

  print("Failed to parse JSON after " + maxRetries + " attempts: " + fullpath);
  return null;
}

function process_new_file(dir_to_check) {
  // Create a directory object
  var dir = new Dir(dir_to_check);

  var fileList = dir.entryList("*.json", Dir.Files | Dir.NoSymLinks, Dir.Name);

  if (fileList.length == 0) {
    return; // nothing to process
  }
  var lowestNum = Number(strip_json(fileList[0]));

  for (var i = 1; i < fileList.length; ++i) {
    var f = fileList[i];
    var num = Number(strip_json(f));
    if (num < lowestNum) {
      lowestNum = num;
      lowestFile = f;
    }
  }

  var filePath = dir_to_check + "/" + lowestNum + ".json";
  return filePath;
}

function strip_json(filename) {
  var len = filename.length;
  if (len > 5 && filename.substr(len - 5, 5) === ".json") {
    return filename.substr(0, len - 5);
  }
  return filename;
}

function clearLists(timeoutMs, sleepMs) {
  timeoutMs = timeoutMs || 5000;
  sleepMs = sleepMs || 50;
  var startTime = new Date().getTime();

  var proj = App.getActiveProject();
  if (!proj) {
    return false;
  }

  var waveformlist, componentlist, geo_assembly, mat_list;
  try {
    waveformlist = proj.getWaveformList();
    componentlist = proj.getCircuitComponentList();
    geo_assembly = proj.getGeometryAssembly();
    mat_list = proj.getMaterialList();

    if (waveformlist) waveformlist.clear();
    if (componentlist) componentlist.clear();
    if (geo_assembly) geo_assembly.clear();
    if (mat_list) mat_list.clear();

    clearAllCircuitComponentDefinitions();
  } catch (e) {
    print("clearLists initial error: " + e);
    return false;
  }

  // poll just a few times to confirm empty
  while (new Date().getTime() - startTime < timeoutMs) {
    try {
      var w = waveformlist ? waveformlist.getAllWaveformNames().length : 0;
      var c = componentlist
        ? componentlist.getAllCircuitComponentNames().length
        : 0;
      var g = geo_assembly ? geo_assembly.getPartCount() : 0;
      var m = mat_list ? mat_list.getAllMaterialNames().length : 0;

      if (w === 0 && c === 0 && g === 0 && m === 0) {
        return true;
      }
    } catch (e) {
      print("clearLists polling error: " + e);
      return false;
    }

    App.sleep(sleepMs);
  }

  return false;
}

function clearAllCircuitComponentDefinitions() {
  var proj = App.getActiveProject();
  if (!proj) {
    print("clearAllCircuitComponentDefinitions: no active project");
    return;
  }

  var list;
  try {
    list = proj.getCircuitComponentDefinitionList();
    if (!list) return;

    var names = list.getAllCircuitComponentDefinitionNames();
    if (!names) return;

    for (var i = 0; i < names.length; i++) {
      try {
        list.removeCircuitComponentDefinition(names[i]);
      } catch (e) {
        print("Failed to remove component '" + names[i] + "': " + e);
      }
    }
  } catch (e) {
    print("clearAllCircuitComponentDefinitions error: " + e);
  }
}

function updateNextSimulationNumber(indv) {
  var proj_dir = App.getActiveProject().getProjectDirectory();
  var filePath =
    proj_dir.replace(/\/+$/, "") + "/Simulations/.nextSimulationNumber";

  // Check if the file exists
  if (!File.exists(filePath)) {
    return;
  }

  // Remove the old file
  File.remove(filePath);

  // Write the new number
  File.write(filePath, String(indv));
}
