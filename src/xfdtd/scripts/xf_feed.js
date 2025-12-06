function create_feeds(setup_data) {
  // Creates feeds in waveguide
  if (setup_data.units == " cm") {
    var unit_scale = 0.01;
  }
  var indvdata = setup_data.indvdata;
  var half_wg_height =
    (MathUtils.evaluate(indvdata.waveguide_height) / 2) * unit_scale;
  var wg_width = MathUtils.evaluate(indvdata.waveguide_width) * unit_scale;
  var wg_length = MathUtils.evaluate(indvdata.waveguide_length) * unit_scale;
  // Here we will create our waveform, create our circuit component definition for the feed, and create
  // a CircuitComponent that will attach those to our current geometry.
  var waveformList = App.getActiveProject().getWaveformList();
  // clear the waveform list
  waveformList.clear();

  // Create a gaussian derivative input wave
  var waveform = new Waveform();
  var GDer = new GaussianDerivativeWaveformShape();
  GDer.pulseWidth = 8e-9; // NOTE: Changed to reflect new freq range
  waveform.setWaveformShape(GDer);
  waveform.name = "Gaussian Derivative";
  var waveformInList = waveformList.addWaveform(waveform);

  // Now to create the circuit component definition:
  var componentDefinitionList =
    App.getActiveProject().getCircuitComponentDefinitionList();
  // clear the list
  componentDefinitionList.clear();

  // Create our Feed
  var feed1 = new Feed();
  var feed2 = new Feed();

  feed1.feedType = Feed.Voltage; // Set its type enumeration to be Voltage.
  //feed2.feedType = Feed.Voltage; // Set its type enumeration to be Voltage.

  // Define a 50-ohm resistance for this feed
  var rlc = new RLCSpecification();
  rlc.setResistance("50 ohm");
  rlc.setCapacitance("0");
  rlc.setInductance("0");
  feed1.setImpedanceSpecification(rlc);
  feed1.setWaveform(waveformInList); // Make sure to use the reference that was returned by the list, or query the list directly
  feed1.name = "50-Ohm Voltage Source";
  var feedInList = componentDefinitionList.addCircuitComponentDefinition(feed1);

  feed2.setImpedanceSpecification(rlc);
  feed2.setWaveform(waveformInList); // Make sure to use the reference that was returned by the list, or query the list directly
  feed2.name = "50-Ohm Voltage Source 2";
  var feedInList = componentDefinitionList.addCircuitComponentDefinition(feed2);

  // Now create a circuit component that will be the feed point for our simulation
  var componentList = App.getActiveProject().getCircuitComponentList();
  componentList.clear();

  var component1 = new CircuitComponent();
  //var component2 = new CircuitComponent();

  component1.name = "Source";
  //component2.name = "Source";

  component1.setAsPort(true);
  //component2.setAsPort( true );
  var coordinate1 = new CoordinateSystemPosition(
    -MathUtils.evaluate(wg_width) / 2,
    0,
    -half_wg_height
  );
  var coordinate2 = new CoordinateSystemPosition(
    MathUtils.evaluate(wg_width) / 2,
    0,
    -half_wg_height
  );

  //var coordinate3 = new CoordinateSystemPosition( 0, -x2, height);
  //var coordinate4 = new CoordinateSystemPosition( 0, x2, height);
  component1.setCircuitComponentDefinition(feed1);
  component1.setCircuitComponentDefinition(feed1);
  component1.setEndpoint1(coordinate1);
  component1.setEndpoint2(coordinate2);
  /*
    component2.setCircuitComponentDefinition( feed2 );
    component2.setCircuitComponentDefinition( feed2 );
    component2.setEndpoint1( coordinate3 );
    component2.setEndpoint2( coordinate4 );
*/
  componentList.addCircuitComponent(component1);
  //componentList.addCircuitComponent( component2 );
}
