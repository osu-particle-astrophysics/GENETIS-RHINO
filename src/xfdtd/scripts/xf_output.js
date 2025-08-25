// functions dealing with outputs from xfdtd
function xf_output(indv_dir, gaintype, indv_num, num_freqs) {
  // outputs files from XFdtd
  var rb = App.getResultBrowser();
  rb.addProject(App.getActiveProject().getProjectDirectory());

  var simlength = indv_num.toString().length;
  var totchars = 6;
  var init = "";
  for (var i = 0; i < totchars - simlength; i++) {
    init = init + "0";
  }
  var sim_num = init + indv_num;

  while (true) {
    try {
      rb.refresh(ResultBrowser.FullRefreshType);

      var query = new ResultQuery();
      query.projectId = App.getActiveProject().getProjectDirectory();
      query.runId = "Run0001";
      query.simulationId = sim_num;
      query.sensorType = ResultQuery.FarZoneSensor;
      query.sensorId = "Far Zone Sensor";
      query.timeDependence = ResultQuery.SteadyState;

      if (gaintype == "Ideal") {
        query.resultType = ResultQuery.Gain;
      } else if (gaintype == "Realized") {
        query.resultType = ResultQuery.RealizedGain;
      }

      query.fieldScatter = ResultQuery.TotalField;
      query.resultComponent = ResultQuery.Theta;
      query.dataTransform = ResultQuery.NoTransform;
      query.complexPart = ResultQuery.NotComplex;
      query.surfaceInterpolationResolution = ResultQuery.NoInterpolation;
      query.setDimensionRange("Frequency", 0, -1);
      query.setDimensionRange("Theta", 0, -1);
      query.setDimensionRange("Phi", 0, -1);

      var thdata = new ResultDataSet("");
      thdata.setQuery(query);

      query.resultComponent = ResultQuery.Phi;
      var phdata = new ResultDataSet("");
      phdata.setQuery(query);

      // Theta phase
      query.resultType = ResultQuery.E;
      query.fieldScatter = ResultQuery.TotalField;
      query.resultComponent = ResultQuery.Theta;
      query.complexPart = ResultQuery.Phase;
      var thphase = new ResultDataSet("");
      thphase.setQuery(query);

      // Phi phase
      query.resultComponent = ResultQuery.Phi;
      var phphase = new ResultDataSet("");
      phphase.setQuery(query);

      // Input power
      query.sensorType = ResultQuery.System;
      query.sensorId = "System";
      query.resultType = ResultQuery.NetInputPower;
      query.fieldScatter = ResultQuery.NoFieldScatter;
      query.resultComponent = ResultQuery.Scalar;
      query.complexPart = ResultQuery.NotComplex;
      query.clearDimensions();
      query.setDimensionRange("Frequency", 0, -1);

      var inputpower = new ResultDataSet("");
      inputpower.setQuery(query);

      // VSWR
      query.sensorType = ResultQuery.CircuitComponent;
      query.sensorId = "Source";
      query.timeDependence = ResultQuery.SteadyState;
      query.resultType = ResultQuery.VSWR;
      query.fieldScatter = ResultQuery.NoFieldScatter;
      query.resultComponent = ResultQuery.Scalar;
      query.dataTransform = ResultQuery.NoTransform;
      query.complexPart = ResultQuery.NotComplex;
      query.surfaceInterpolationResolution = ResultQuery.NoInterpolation;
      query.setDimensionRange("Frequency", 0, -1);

      var vswr = new ResultDataSet("");
      vswr.setQuery(query);

      // S11
      query.sensorType = ResultQuery.CircuitComponent;
      query.sensorId = "Source";
      query.timeDependence = ResultQuery.SteadyState;
      query.resultType = ResultQuery.ReflectionCoefficient;
      query.fieldScatter = ResultQuery.NoFieldScatter;
      query.resultComponent = ResultQuery.Scalar;
      query.dataTransform = ResultQuery.NoTransform;
      query.complexPart = ResultQuery.ComplexMagnitude;
      query.surfaceInterpolationResolution = ResultQuery.NoInterpolation;
      query.setDimensionRange("Frequency", 0, -1);

      var s11 = new ResultDataSet("");
      s11.setQuery(query);

      // Impedence
      query.sensorType = ResultQuery.CircuitComponent;
      query.sensorId = "Source";
      query.timeDependence = ResultQuery.SteadyState;
      query.resultType = ResultQuery.Impedance;
      query.fieldScatter = ResultQuery.NoFieldScatter;
      query.resultComponent = ResultQuery.Scalar;
      query.dataTransform = ResultQuery.NoTransform;
      query.complexPart = ResultQuery.ComplexMagnitude;
      query.surfaceInterpolationResolution = ResultQuery.NoInterpolation;
      query.setDimensionRange("Frequency", 0, -1);

      var imp = new ResultDataSet("");
      imp.setQuery(query);

      if (typeof outpath === "undefined") {
        var ind_num = k - gen * popsize;
        var file = RunDir + "/csv_files/";
        file = file + gen + "_" + ind_num;
        file = file + "_vswr_s11_imp.csv";
      } else {
        var file = outpath + "/1_1_vswr_s11_imp.csv";
      }

      // Check validity
      if (
        thdata.isValid() &&
        phdata.isValid() &&
        thphase.isValid() &&
        phphase.isValid() &&
        inputpower.isValid() &&
        vswr.isValid() &&
        s11.isValid() &&
        imp.isValid()
      ) {
        // Export uan files
        for (var i = 1; i <= num_freqs; i++) {
          var file = indv_dir + "/uan_files/" + indv_num + "_" + i + ".uan";
          FarZoneUtils.exportToUANFile(
            thdata,
            thphase,
            phdata,
            phphase,
            inputpower,
            file,
            i - 1
          );
        }
        // Export VSWR, S11, Imp into csv file
        var file = indv_dir + "/vswr_s11_imp.csv";
        var csv_file = new File(file);
        csv_file.open(IODevice.WriteOnly);

        DataSetExportUtility.exportDataSetCsv(
          csv_file,
          [vswr, s11, imp],
          false
        );
        csv_file.close();
        Output.println("Outputted files from individual " + indv_num);
        break;
      } else {
        Output.println("Data invalid, retrying...");
      }
    } catch (err) {
      Output.println("Error during export: " + err);
    }

    App.sleep(1000); // 1 second
  }
}
