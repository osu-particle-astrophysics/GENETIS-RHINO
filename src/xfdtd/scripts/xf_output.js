// functions dealing with outputs from xfdtd
function xf_output(indv_dir, indv_num, num_freqs) {
  // outputs UAN files from XFdtd (minimal-safe)
  var projDir = App.getActiveProject().getProjectDirectory();
  var rb = null;

  // ensure result browser knows about this project at least once
  try {
    rb = App.getResultBrowser();
    if (rb && typeof rb.addProject === "function") {
      // addProject may be idempotent or a no-op if already present
      rb.addProject(projDir);
    }
  } catch (e) {
    print("xf_output: warning adding project to ResultBrowser: " + e);
  }

  var simlength = indv_num.toString().length;
  var totchars = 6;
  var init = "";
  for (var i = 0; i < totchars - simlength; i++) init += "0";
  var sim_num = init + indv_num;

  // Retry loop parameters
  var attempt = 0;
  var maxRetries = 300; // (300 * sleepMs = total wait)
  var sleepMs = 1000; // 1 second between attempts

  while (attempt < maxRetries) {
    attempt++;

    // Re-acquire RB each iteration (in case previous handle got invalidated)
    try {
      rb = App.getResultBrowser();
    } catch (e) {
      print("xf_output: cannot get ResultBrowser: " + e);
      // wait and retry
      App.sleep(sleepMs);
      continue;
    }

    // Try calling refresh only if we have a valid object and function
    try {
      if (rb && typeof rb.refresh === "function") {
        try {
          rb.refresh(ResultBrowser.FullRefreshType);
        } catch (e) {
          // If refresh fails because the underlying QObject was deleted,
          // try one recovery: re-add the project to result browser and retry.
          print(
            "xf_output: rb.refresh failed on attempt " + attempt + ": " + e
          );
          try {
            if (typeof rb.addProject === "function") rb.addProject(projDir);
          } catch (inner) {
            print("xf_output: rb.addProject also failed: " + inner);
          }
          // wait then loop to try again (unless we've hit maxRetries)
          App.sleep(sleepMs);
          continue;
        }
      } else {
        // rb doesn't expose refresh: attempt to re-register the project then continue
        if (rb && typeof rb.addProject === "function") {
          try {
            rb.addProject(projDir);
          } catch (e) {
            print("xf_output: rb.addProject failed: " + e);
          }
        }
      }
    } catch (e) {
      // catch anything unexpected from rb handling
      print("xf_output: unexpected error with ResultBrowser: " + e);
      App.sleep(sleepMs);
      continue;
    }

    // Build queries and result datasets
    try {
      var query = new ResultQuery();
      query.projectId = projDir;
      query.runId = "Run0001";
      query.simulationId = sim_num;
      query.sensorType = ResultQuery.FarZoneSensor;
      query.sensorId = "Far Zone Sensor";
      query.timeDependence = ResultQuery.SteadyState;

      query.resultType = ResultQuery.RealizedGain; // Jacob - I'm assuming for RHINO we ALWAYS want Realized gain.

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

      // Check validity and export
      if (
        thdata.isValid() &&
        phdata.isValid() &&
        thphase.isValid() &&
        phphase.isValid() &&
        inputpower.isValid()
      ) {
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

        print("Outputted files from individual " + indv_num);
        return true;
      } else {
        print("Data invalid, retrying...");
        App.sleep(1000);
      }
    } catch (err) {
      print("Error during export: " + err);
    }

    // short pause — avoid very tight loop but don't block GUI too long
    App.sleep(sleepMs);
  }

  if (attempt >= maxRetries) {
    print("xf_output: max retries reached (" + maxRetries + "), aborting.");
    return false;
  }
}
