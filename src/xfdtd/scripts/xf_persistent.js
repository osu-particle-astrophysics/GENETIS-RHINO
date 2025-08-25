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

      xf_setup(setup_data);
    }

    // Check diretory for output file
    var output_file = process_new_file(output_dir);
    if (output_file != null && output_file != "") {
      var output_data = jsonparse(output_file);

      xf_output(
        output_data.indv_dir,
        output_data.gaintype,
        output_data.indv_num,
        output_data.num_freqs
      );
    }
  }
}

function xf_setup(setup_data) {
  // Function calls to setup xfdtd simulation and build antenna

  App.getActiveProject().getGeometryAssembly().clear();
  App.getActiveProject().getMaterialList().clear();

  build_walls(setup_data);
  build_ridges(setup_data);
  build_waveguide(setup_data);
  create_feeds(setup_data);

  create_grid(setup_data);
  create_sensors(setup_data);
  create_sim_data(setup_data);
  queue_sim(setup_data);
  make_image(setup_data);
}

function jsonparse(fullpath) {
  // This function will parse in the json file and return the filedata in an XF readable format
  // This is the name of the file

  var file = new File(fullpath);
  file.open(1);
  var data = file.readAll();
  // parsing in the json file
  var filedata = JSON.parse(data);
  // Closing File
  file.close(1);

  // Returning the data
  return filedata;
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
