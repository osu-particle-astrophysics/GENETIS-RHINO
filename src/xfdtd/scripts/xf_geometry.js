// Version of RHINO geometry script for testing
// TODO: Add Ridges
// TODO: Where in waveguides do feeds need to be placed? Currently assuming halfway
// TODO: Do we need two feeds for horizontal and vertical polarizations?
// TODO: Is flare being constructed correctly? I don't totally understand the different angles for wall pairs.
// TODO: Isn't this constructing an Antenna 2x as big as wanted?
// TODO: Is length defined as the y direction and width the x direction?

// XFdtd functions related to building antenna geometry

function build_flare(setup_data) {
  // Makes the outer walls of the horn antenna
  if (setup_data.units == " cm") {
    var unit_scale = 0.01;
  }
  var indvdata = setup_data.indvdata;
  var wg_length = MathUtils.evaluate(indvdata.waveguide_length) * unit_scale;
  var wg_width = MathUtils.evaluate(indvdata.waveguide_width) * unit_scale;
  var wall0_slope = Math.tan(
    (MathUtils.evaluate(indvdata.wall_pair0.angle) * Math.PI) / 180
  );
  if (indvdata.wall_pair1.angle != null) {
    var wall1_slope = Math.tan(
      (MathUtils.evaluate(indvdata.wall_pair1.angle) * Math.PI) / 180
    );
  } else {
    var wall1_slope = wall0_slope;
  }
  var flare_height = MathUtils.evaluate(indvdata.flare_length) * unit_scale;
  Output.println(wall0_slope);
  Output.println(wall1_slope);
  // Edge definitions
  var edge1 = Line(
    new Cartesian3D(-wg_width, -wg_length, 0),
    new Cartesian3D(-wg_width, wg_length, 0)
  );
  var edge2 = Line(
    new Cartesian3D(-wg_width, wg_length, 0),
    new Cartesian3D(wg_width, wg_length, 0)
  );
  var edge3 = Line(
    new Cartesian3D(wg_width, wg_length, 0),
    new Cartesian3D(wg_width, -wg_length, 0)
  );
  var edge4 = Line(
    new Cartesian3D(wg_width, -wg_length, 0),
    new Cartesian3D(-wg_width, -wg_length, 0)
  );

  // Declare sketches to be made from the edges
  var flare_sketch = new Sketch();
  flare_sketch.addEdges([edge1, edge2, edge3, edge4]);

  // Now we need to extrude the edges to get height
  var wall_pair0 = new Extrude(flare_sketch, flare_height); // Makes an Extrude
  var wall_pair1 = new Extrude(flare_sketch, flare_height);
  var wall_pair0_options = wall_pair0.getOptions(); // Gives the possible options for
  var wall_pair1_options = wall_pair1.getOptions();
  // We will use the draft law option to extrude linearly
  wall_pair0_options.draftOption = SweepOptions.DraftLaw; // allows for draftlaw
  wall_pair1_options.draftOption = SweepOptions.DraftLaw;
  wall_pair0_options.draftLaw = "(" + wall0_slope + "*x)"; // Set the expression for the extrude
  wall_pair1_options.draftLaw = "(" + wall1_slope + "*x)";
  wall_pair0_options.draftOption = 4; // 4 indicates we use draftlaw
  wall_pair1_options.draftOption = 4;
  //Walter - Change the gap type to Extended to get the desired shape
  wall_pair0_options.gapType = SweepOptions.Extended; // I actually don't like this when we have x^2, but it doesn't do much for just x
  wall_pair1_options.gapType = SweepOptions.Extended;
  //Walter - Create a shell instead of a solid part
  wall_pair0_options.createSolid = false; // This way the shape isn't filled in
  wall_pair1_options.createSolid = false;
  wall_pair0.setOptions(wall_pair0_options); // Sets the settings we assigned above
  wall_pair1.setOptions(wall_pair1_options);

  // Make a recipe for a model
  var wall_pair0_recipe = new Recipe();
  wall_pair0_recipe.append(wall_pair0);
  var wall_pair0_model = new Model();
  wall_pair0_model.setRecipe(wall_pair0_recipe);
  wall_pair0_model.name = "Wall Pair 0 Flare";
  wall_pair0_model.getCoordinateSystem().translate(new Cartesian3D(0, 0, 0)); // Makes the model start at the origin
  var wall_pair1_recipe = new Recipe();
  wall_pair1_recipe.append(wall_pair0);
  var wall_pair1_model = new Model();
  wall_pair1_model.setRecipe(wall_pair0_recipe);
  wall_pair1_model.name = "Wall Pair 1 Flare";
  wall_pair1_model.getCoordinateSystem().translate(new Cartesian3D(0, 0, 0)); // Makes the model start at the origin

  // Set the material for these parts
  var flare_project = App.getActiveProject()
    .getGeometryAssembly()
    .append(wall_pair0_model); // Adds the model to the project
  var pec_material = App.getActiveProject()
    .getMaterialList()
    .getMaterial("PEC");
  App.getActiveProject().setMaterial(flare_project, pec_material);
  var flare_project = App.getActiveProject()
    .getGeometryAssembly()
    .append(wall_pair1_model);
  App.getActiveProject().setMaterial(flare_project, pec_material);
}

function build_waveguide(setup_data) {
  // Make a waveguide
  if (setup_data.units == " cm") {
    var unit_scale = 0.01;
  }
  var indvdata = setup_data.indvdata;
  var wg_length = MathUtils.evaluate(indvdata.waveguide_length) * unit_scale;
  var wg_width = MathUtils.evaluate(indvdata.waveguide_width) * unit_scale;
  var wg_height = MathUtils.evaluate(indvdata.waveguide_height) * unit_scale;
  // Make the edges to define the square
  var edge1 = Line(
    new Cartesian3D(-wg_width, -wg_length, 0),
    new Cartesian3D(-wg_width, wg_length, 0)
  );
  var edge2 = Line(
    new Cartesian3D(-wg_width, wg_length, 0),
    new Cartesian3D(wg_width, wg_length, 0)
  );
  var edge3 = Line(
    new Cartesian3D(wg_width, wg_length, 0),
    new Cartesian3D(wg_width, -wg_length, 0)
  );
  var edge4 = Line(
    new Cartesian3D(wg_width, -wg_length, 0),
    new Cartesian3D(-wg_width, -wg_length, 0)
  );

  // Declare sketches to be made from the edges
  var wall_sketch = new Sketch();
  wall_sketch.addEdges([edge1, edge2, edge3, edge4]);

  // Now we need to extrude the edges to get height
  var wall_extrude = new Extrude(wall_sketch, -wg_height); // Makes an Extrude
  var wall_options = wall_extrude.getOptions(); // Gives the possible options for
  // We will use the draft law option to extrude linearly
  wall_options.draftOption = SweepOptions.DraftLaw; // allows for draftlaw
  wall_options.draftLaw = "(-1)"; // Set the expression for the extrude
  wall_options.draftOption = 4; // 4 indicates we use draftlaw
  //Walter - Change the gap type to Extended to get the desired shape
  wall_options.gapType = SweepOptions.Extended; // I actually don't like this when we have x^2, but it doesn't do much for just x
  //Walter - Create a shell instead of a solid part
  wall_options.createSolid = false; // This way the shape isn't filled in
  wall_extrude.setOptions(wall_options); // Sets the settings we assigned above

  // Make a recipe for a model
  var wall_recipe = new Recipe();
  wall_recipe.append(wall_extrude);
  var wall_model = new Model();
  wall_model.setRecipe(wall_recipe);
  wall_model.name = "Waveguide";
  wall_model.getCoordinateSystem().translate(new Cartesian3D(0, 0, 0)); // Makes the model start at the origin

  // Set the material for these parts
  var wall_project = App.getActiveProject()
    .getGeometryAssembly()
    .append(wall_model); // Adds the model to the project
  var pec_material = App.getActiveProject()
    .getMaterialList()
    .getMaterial("PEC");
  App.getActiveProject().setMaterial(wall_project, pec_material);
}

// Builds the ridges
// Here are the arguments, which are primarily used when making the LawEdges
// Bottom x: distance from center
// Bottom y: distance from center
// Bottom z: distance from center (keep to 0)
// Top x: distance from center
// Top y: distance from center
// Top z: distance from center
// tau: Arbitrary time limit used for the parametric curves (the ridge shapes)
// beta: determines the curvature of the ridges
// S: Side length of bottom of walls
// m: Slope of walls (currently set to 1)
function build_ridges(x_0, y_0, z_0, x_f, y_f, z_f, tau, beta, S, m) {
  // Curves (Z is logarithmic in t)
  var Log1 = new LawEdge(
    "" + x_0 + " + (" + z_f + "-" + x_0 + ")/" + tau + "*u",
    "" + y_0 + " + (" + y_f + "-" + y_0 + ")/" + tau + "*u",
    "" + beta + "*ln((exp(" + z_f + "/" + beta + ")-1.0)/" + tau + "*u+1.0)",
    0,
    tau
  );
  var Log2 = new LawEdge(
    "" + x_0 + " + (" + z_f + "-" + x_0 + ")/" + tau + "*u",
    "-" + y_0 + " - (" + y_f + "-" + y_0 + ")/" + tau + "*u",
    "" + beta + "*ln((exp(" + z_f + "/" + beta + ")-1.0)/" + tau + "*u+1.0)",
    0,
    tau
  );

  // Inner straight slopes
  var IS1 = new LawEdge(
    "" + x_0 + " + (" + z_f + "-" + x_0 + ")/" + tau + "*u",
    "" + y_0 + " + (" + y_f + "-" + y_0 + ")/" + tau + "*u",
    "(" + z_f + "-" + z_0 + ")/" + tau + "*u",
    0,
    tau
  );
  var IS2 = new LawEdge(
    "" + x_0 + " + (" + z_f + "-" + x_0 + ")/" + tau + "*u",
    "-" + y_0 + " - (" + y_f + "-" + y_0 + ")/" + tau + "*u",
    "(" + z_f + "-" + z_0 + ")/" + tau + "*u",
    0,
    tau
  );

  // Bottom line
  var BL1 = new LawEdge(
    "" + x_0 + " + (" + x_f + "-" + x_0 + ")/" + tau + "*u",
    "" + y_0 + "",
    "" + z_0 + "",
    0,
    tau
  );
  var BL2 = new LawEdge(
    "" + x_0 + " + (" + x_f + "-" + x_0 + ")/" + tau + "*u",
    "-" + y_0 + "",
    "" + z_0 + "",
    0,
    tau
  );

  // Top line
  var TL1 = new LawEdge(
    "" + z_f + " + " + x_f + "/" + tau + "*u",
    "" + y_f + "",
    "" + z_f + "",
    0,
    tau
  );
  var TL2 = new LawEdge(
    "" + z_f + " + " + x_f + "/" + tau + "*u",
    "-" + y_f + "",
    "" + z_f + "",
    0,
    tau
  );

  // Outer Straight slopes
  var OS1 = new LawEdge(
    "" + x_f + " + " + z_f + "/" + tau + "*u",
    "" + y_0 + " + (" + y_f + " - " + y_0 + ")/" + tau + "*u",
    "" + z_f + "/" + tau + "*u",
    0,
    tau
  );
  var OS2 = new LawEdge(
    "" + x_f + " + " + z_f + "/" + tau + "*u",
    "-" + y_0 + " - (" + y_f + " - " + y_0 + ")/" + tau + "*u",
    "" + z_f + "/" + tau + "*u",
    0,
    tau
  );

  // Inner top line
  var ITL = new LawEdge(
    "" + z_f + "",
    "-" + y_f + " + 2*" + y_f + "/" + tau + "*u",
    "" + z_f + "",
    0,
    tau
  );

  // Outer top line
  var OTL = new LawEdge(
    "" + x_f + " + " + z_f + "",
    "-" + y_f + " + 2*" + y_f + "/" + tau + "*u",
    "" + z_f + "",
    0,
    tau
  );

  // Inner bottom line
  var IBL = new LawEdge(
    "" + x_0 + "",
    "-" + y_0 + " + 2*" + y_0 + "/" + tau + "*u",
    "" + z_0 + "",
    0,
    tau
  );

  // Outer bottom line
  var OBL = new LawEdge(
    "" + x_f + "",
    "-" + y_0 + " + 2*" + y_0 + "/" + tau + "*u",
    "" + z_0 + "",
    0,
    tau
  );

  // Make the sketches
  var straightEdge1 = new Sketch(); // All straight edges (IS1, BL1, TL1, OS1)
  var straightEdge2 = new Sketch(); // All straight edges (IS2, BL2, TL2, OS2)
  var curvedLog1 = new Sketch(); // Logarithmic edge (IS1 and Log1)
  var curvedLog2 = new Sketch(); // Logarithmic edge (IS2 and Log2)
  var topRectangle = new Sketch(); // Top rectangle
  var bottomRectangle = new Sketch(); // Bottom rectangle

  // Add the edges to the sketches
  straightEdge1.addEdges([IS1, BL1, TL1, OS1]); // Inner straight slope
  curvedLog1.addEdges([IS1, Log1]); // Right logarithm part
  straightEdge2.addEdges([IS2, BL2, TL2, OS2]); // Inner straight slope
  curvedLog2.addEdges([IS2, Log2]); // Left logarithm part
  topRectangle.addEdges([ITL, OTL, TL1, TL2]); // Top rectangle
  bottomRectangle.addEdges([IBL, OBL, BL1, BL2]); // Bottom Rectangle

  //WALTER - The Elliptical pattern is added as a recipe to the parts
  //In this case the location of the center and direction of the normal are simple, but for more complex scenarios, may need to use more functionality to find them.
  var ePattern = new EllipticalPattern();
  ePattern.setCenter(new CoordinateSystemPosition(0, 0, 0));
  ePattern.setNormal(new CoordinateSystemDirection(0, 0, 1));
  ePattern.setInstances(num_ridges);
  ePattern.setRotated(true);

  // Create an array of covers (used for making the ridges solid/closed)
  var cov = new Array();
  cov.push(new Cover(straightEdge1));
  cov.push(new Cover(straightEdge2));
  cov.push(new Cover(curvedLog1));
  cov.push(new Cover(curvedLog2));
  cov.push(new Cover(topRectangle));
  cov.push(new Cover(bottomRectangle));

  var pecMaterial = App.getActiveProject().getMaterialList().getMaterial("PEC");

  //WALTER - We can loop over all our parts and add them to the project as follows.  You can use similar concepts above.
  models = new Assembly();
  for (var w = 0; w < cov.length; w++) {
    var r = new Recipe();
    r.append(cov[w]);
    r.append(ePattern);
    var m = new Model();
    m.setRecipe(r);
    m.name = "Test Surface " + (w + 1);
    //WALTER - Seperate array for the models, though we could just get them from the GemoetryAssembly again
    models.append(m);
    App.getActiveProject().setMaterial(m, pecMaterial);
  }

  // Work on the loft
  var vertex_position1 = curvedLog1.getPosition(curvedLog1.getVertexIds()[0]);
  var vertex_position2 = curvedLog2.getPosition(curvedLog2.getVertexIds()[0]);

  var loft = new Loft(
    models.at(2).pickFace(new Cartesian3D(0, 0, 0), vertex_position1, 0.5),
    "0.0",
    models.at(3).pickFace(new Cartesian3D(0, 0, 0), vertex_position2, 0.5),
    "0.0"
  );
  loft.setPart1(models.at(2));
  loft.setPart2(models.at(3));

  var r12 = new Recipe();
  r12.append(loft);
  r12.append(ePattern);
  var m12 = new Model();
  m12.setRecipe(r12);
  m12.name = "Loft 1";
  models.append(m12);

  //WALTER - append the assembly to the project, then loop over it to assign the material
  var assembly = App.getActiveProject().getGeometryAssembly().append(models);
  for (x = 0; x < assembly.size(); x++) {
    Output.println(assembly.at(x));
    App.getActiveProject().setMaterial(assembly.at(x), pecMaterial);
  }
}
