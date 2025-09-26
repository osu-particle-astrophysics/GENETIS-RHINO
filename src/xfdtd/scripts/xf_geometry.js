var sym_count = 0;
var num_ridges = 4; // either 2 or 4

// Order of genes:
// S, H, x0, y0, xf, yf, zf, beta
var Tau = 0.26; // Normalized parametric time--no good reason to be 0.26, but it's fine

var height1 = 0.01; // Where we place the second power source; needs to not intersect the first one!
var height2 = 0.06; // Where we place the second power source; needs to not intersect the first one!

// Lists to hold the genes
// Potential genes:
// Number of side lengths (start with fixing at 2), number of wall sections, side length dimensions, opening angle(s), full height, waveguide depth, source height (in waveguide), ridge dimensions, additional wall parameters (new opening angles, height)

/* Genes for wall pairs
		:param angle: The angle of the wall pair. Must be between 0 and 90
        degrees. Defaults to None.
        :type angle: float, optional
        :param ridge_height: The flare_height of the ridge as a percentage of the
        total horn flare_height. Starts from bottom of horn. Must be between 0%
        and 100%(inclusive).
        :type ridge_height: float, optional
        :param ridge_width_top: The width of the ridge at the top of the horn.
        Must be between 0 cm and 100 cm (inclusive).
        :type ridge_width_top: float, optional
        :param ridge_width_bottom: The width of the ridge at the bottom of
        the .
        Must be between 0 cm and 100 cm (inclusive).
        :type ridge_width_bottom: float, optional
        :param ridge_thickness_top: The thickness of the ridge. Must be
        between 0 cm
        and 100 cm (inclusive).
        :type ridge_thickness_top: float, optional
        :param ridge_thickness_bottom: The thickness of the ridge at the
        bottom of the . Must be between 0 cm and 100 cm (inclusive).
        :type ridge_thickness_bottom: float, optional
        :rtype: None

		self.has_ridge = False
        self.angle = angle
        :param flare_length: The length of the antenna's flare
        :type flare_length: float, optional
        :param waveguide_height: The flare_height of the waveguide.
        :type waveguide_height: float, optional
        :param waveguide_length: The length of the waveguide.
        :type waveguide_length: float, optional
        :param waveguide_width: The length of the waveguide.
        :type waveguide_width: float, optional
        :param walls: A list of WallPair objects that comprise the walls of the
        antenna.

*/

/* Wall Genes */
var num_walls = [];
var angle1 = [];
var angle2 = [];
var wall_height1 = [];
var wall_height2 = [];
var wall_width1 = [];
var wall_length1 = [];
var wall_width2 = [];
var wall_length2 = [];

/* Ridge Genes */
var has_ridge = [];
var ridge_height = [];
var ridge_width_top = [];
var ridge_width_bottom = [];
var ridge_thickness_top = [];
var ridge_thickness_bottom = [];

/* Waveguide Genes*/
var waveguide_depth = [];

/* Original Genes */

var S = []; // Side length of bottom of antenna
//var m=[];
var H = []; // Height of antenna
var X0 = []; // distance from center of ridges at bottom // previously 0.04
var Y0 = []; // (half) width of ridges at bottom // previously 0.04
var Z0 = []; // initial height of ridges (0 always for now)
var Xf = []; // final distance from center of curve of ridges at max height
var Yf = []; // final width of ridges at max height
var Zf = []; // max height of ridges
var Beta = []; // curvature of ridges
var L = []; // (half) width of minor length of trapezoid extrude
var h = []; // "height" of trapezoid extrude (in x-y plane; must be < x0)

for (var i = indiv - 1; i < NPOP; i++) {
  /* Original */
  var s = S[i];
  var ah = H[i];
  var x0 = X0[i];
  var y0 = Y0[i];
  var z0 = 0;
  var xf = s; // By constraint
  var yf = Yf[i];
  var zf = Zf[i];
  var beta = Beta[i];
  var l = L[i];
  var th = h[i];
  var m = 1; // Adjust this to read in the angle from the csv and convert to slope
  var d = 0.03;

  /* RHINO */
  var N = num_walls[i];
  var s1 = wall_length1[i];
  var s2 = wall_length2[i];
  var h1 = wall_height1[i];
  var h2 = wall_height2[i];
  var m1 = Math.tan((angle1[i] * Math.PI) / 180);
  var m2 = Math.tan((angle2[i] * Math.PI) / 180);
  /* Wall Genes */
  var ridge = has_ridge[i];
  var rh1 = has_ridge[i];
  var rwt = ridge_width_top[i];
  var rwb = ridge_width_bottom[i];
  var rtt = ridge_thickness_top[i];
  var rtb = ridge_thickness_bottom[i];
  /* Waveguide */
  var wgd = waveguide_depth[i];

  // Function calls
  // We do it twice, first for horizontal source then for vertical
  for (var k = 0; k <= sym_count; k++) {
    if (k == 0) {
      height = -height1;
    } else {
      height = -height2;
    }
    T = (Tau / (Math.exp(zf / beta) - 1)) * (Math.exp(height / beta) - 1);
    X = 1 * x0 + ((zf - x0) / Tau) * T; // Multiply x0 by 1 because otherwise it doesn't know it's a number lol

    //l = (x0-y0)/4; //arbitrary

    build_waveguide(1 * s1, 1 * s1, 1 * s1, -1 * wgd);

    build_walls(s1, m1, h1, 0);
    if (N == 1) {
      build_walls(s2, m2, 1 * h2, 1 * ah);
    }
  }
}

function build_walls(S, m, H, z0) {
  // Makes the outer walls of the horn antenna
  // S is the side length of the bottom of the wall
  // m is the coefficient for the linear function the walls extrude according to (currently set to 1)
  // H is the final height of the walls

  // Make the edges to define the square
  var edge1 = Line(new Cartesian3D(-S, -S, 0), new Cartesian3D(-S, S, 0));
  var edge2 = Line(new Cartesian3D(-S, S, 0), new Cartesian3D(S, S, 0));
  var edge3 = Line(new Cartesian3D(S, S, 0), new Cartesian3D(S, -S, 0));
  var edge4 = Line(new Cartesian3D(S, -S, 0), new Cartesian3D(-S, -S, 0));

  // Declare sketches to be made from the edges
  var wallSegment = new Sketch();
  var bottomSegment = new Sketch();
  wallSegment.addEdge(edge1);
  wallSegment.addEdge(edge2);
  wallSegment.addEdge(edge3);
  wallSegment.addEdge(edge4);

  bottomSegment.addEdge(edge1);
  bottomSegment.addEdge(edge2);
  bottomSegment.addEdge(edge3);
  bottomSegment.addEdge(edge4);

  // Let's start by making the bottom
  var bottomCover = new Cover(bottomSegment);
  var bottomRecipe = new Recipe();
  bottomRecipe.append(bottomCover);
  var bottomModel = new Model();
  bottomModel.setRecipe(bottomRecipe);
  // Add the surface
  //var bottom = App.getActiveProject().getGeometryAssembly().append(bottomModel);
  //bottom.name = "Bottom square";

  // Now we need to extrude the edges to get height
  var walls = new Extrude(wallSegment, H); // Makes an Extrude
  var wallOptions = walls.getOptions(); // Gives the possible options for
  // We will use the draft law option to extrude linearly
  wallOptions.draftOption = SweepOptions.DraftLaw; // allows for draftlaw
  wallOptions.draftLaw = "(" + m + "*x)"; // Set the expression for the extrude
  wallOptions.draftOption = 4; // 4 indicates we use draftlaw
  //Walter - Change the gap type to Extended to get the desired shape
  wallOptions.gapType = SweepOptions.Extended; // I actually don't like this when we have x^2, but it doesn't do much for just x
  //Walter - Create a shell instead of a solid part
  wallOptions.createSolid = false; // This way the shape isn't filled in
  walls.setOptions(wallOptions); // Sets the settings we assigned above

  // Make a recipe for a model
  var wallRecipe = new Recipe();
  wallRecipe.append(walls);
  var wallModel = new Model();
  wallModel.setRecipe(wallRecipe);
  wallModel.name = "Outer Walls";
  //wallModel.getCoordinateSystem().translate(new Cartesian3D(0,0,0));	// Makes the model start at the origin
  wallModel.getCoordinateSystem().translate(new Cartesian3D(0, 0, z0)); // Makes the model start at the origin
  // Set the material for these parts
  var wallProject = App.getActiveProject()
    .getGeometryAssembly()
    .append(wallModel); // Adds the model to the project
  var pecMaterial = App.getActiveProject().getMaterialList().getMaterial("PEC"); // Makes the material available
  App.getActiveProject().setMaterial(wallProject, pecMaterial); // Sets the material
  //App.getActiveProject().setMaterial( bottom, pecMaterial );						// Sets the material
} // end buil_walls

function build_ridges(x_0, y_0, z_0, x_f, y_f, z_f, tau, beta, S, m) {
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

function build_waveguide(S, D) {
  // Make a waveguide
  // D for "depdth"
  // Make the edges to define the square
  var edge1 = Line(new Cartesian3D(-S, -S, 0), new Cartesian3D(-S, S, 0));
  var edge2 = Line(new Cartesian3D(-S, S, 0), new Cartesian3D(S, S, 0));
  var edge3 = Line(new Cartesian3D(S, S, 0), new Cartesian3D(S, -S, 0));
  var edge4 = Line(new Cartesian3D(S, -S, 0), new Cartesian3D(-S, -S, 0));

  // Declare sketches to be made from the edges
  var wallSegment = new Sketch();
  var bottomSegment = new Sketch();
  wallSegment.addEdge(edge1);
  wallSegment.addEdge(edge2);
  wallSegment.addEdge(edge3);
  wallSegment.addEdge(edge4);
  bottomSegment.addEdge(edge1);
  bottomSegment.addEdge(edge2);
  bottomSegment.addEdge(edge3);
  bottomSegment.addEdge(edge4);

  // Let's start by making the bottom
  var bottomCover = new Cover(bottomSegment);
  var bottomRecipe = new Recipe();
  bottomRecipe.append(bottomCover);
  var bottomModel = new Model();
  bottomModel.setRecipe(bottomRecipe);
  // Add the surface
  //var bottom = App.getActiveProject().getGeometryAssembly().append(bottomModel);
  //bottom.name = "Bottom square";

  // Now we need to extrude the edges to get height
  var walls = new Extrude(wallSegment, D); // Makes an Extrude
  var wallOptions = walls.getOptions(); // Gives the possible options for
  // We will use the draft law option to extrude linearly
  wallOptions.draftOption = SweepOptions.DraftLaw; // allows for draftlaw
  wallOptions.draftLaw = "(-1)"; // Set the expression for the extrude
  wallOptions.draftOption = 4; // 4 indicates we use draftlaw
  //Walter - Change the gap type to Extended to get the desired shape
  wallOptions.gapType = SweepOptions.Extended; // I actually don't like this when we have x^2, but it doesn't do much for just x
  //Walter - Create a shell instead of a solid part
  wallOptions.createSolid = false; // This way the shape isn't filled in
  walls.setOptions(wallOptions); // Sets the settings we assigned above

  // Make a recipe for a model
  var wallRecipe = new Recipe();
  wallRecipe.append(walls);
  var wallModel = new Model();
  wallModel.setRecipe(wallRecipe);
  wallModel.name = "Outer Walls";
  wallModel.getCoordinateSystem().translate(new Cartesian3D(0, 0, 0)); // Makes the model start at the origin

  // Set the material for these parts
  var wallProject = App.getActiveProject()
    .getGeometryAssembly()
    .append(wallModel); // Adds the model to the project
  var pecMaterial = App.getActiveProject().getMaterialList().getMaterial("PEC"); // Makes the material available
  App.getActiveProject().setMaterial(wallProject, pecMaterial); // Sets the material
}

function extend_ridges_trapezoid(S, x_0, y_0, D, L, th) {
  // New extensions but with trapezoid shapes
  // We define L as the half length of the minor side of the trapezoid
  // We want the trapezoid to be at 45 degrees from the major base, so we
  //	say the height is y0 - L
  // D for "depdth", L for "Length"
  // Below works for example antenna at l = (x0-y0)/4
  // Make the edges to define the square
  var edge1 = Line(new Cartesian3D(-S, y_0, 0), new Cartesian3D(-x_0, y_0, 0)); // good
  var diag1 = Line(
    new Cartesian3D(-x_0, y_0, 0),
    new Cartesian3D(-x_0 + th, L, 0)
  ); // good
  var edge5 = Line(
    new Cartesian3D(-x_0 + th, L, 0),
    new Cartesian3D(-x_0 + th, -L, 0)
  ); // good
  var diag2 = Line(
    new Cartesian3D(-x_0 + th, -L, 0),
    new Cartesian3D(-x_0, -y_0, 0)
  ); // good
  var edge3 = Line(
    new Cartesian3D(-x_0, -y_0, 0),
    new Cartesian3D(-S, -y_0, 0)
  ); // good
  var edge4 = Line(new Cartesian3D(-S, -y_0, 0), new Cartesian3D(-S, y_0, 0)); // good

  // Declare sketches to be made from the edges
  var wallSegment = new Sketch();
  var bottomSegment = new Sketch();
  wallSegment.addEdge(edge1);
  //	wallSegment.addEdge(edge2);
  wallSegment.addEdge(edge3);
  wallSegment.addEdge(edge4);
  wallSegment.addEdge(diag1);
  wallSegment.addEdge(diag2);
  wallSegment.addEdge(edge5);

  bottomSegment.addEdge(edge1);
  //	bottomSegment.addEdge(edge2);
  bottomSegment.addEdge(edge3);
  bottomSegment.addEdge(edge4);
  bottomSegment.addEdge(diag1);
  bottomSegment.addEdge(diag2);
  bottomSegment.addEdge(edge5);

  // Let's start by making the bottom
  var bottomCover = new Cover(bottomSegment);
  var bottomRecipe = new Recipe();
  bottomRecipe.append(bottomCover);
  var bottomModel = new Model();
  bottomModel.setRecipe(bottomRecipe);
  // Add the surface
  //var bottom = App.getActiveProject().getGeometryAssembly().append(bottomModel);
  //bottom.name = "Bottom square";

  // Now we need to extrude the edges to get height
  var walls = new Extrude(wallSegment, D); // Makes an Extrude
  var wallOptions = walls.getOptions(); // Gives the possible options for
  // We will use the draft law option to extrude linearly
  wallOptions.draftOption = SweepOptions.DraftLaw; // allows for draftlaw
  wallOptions.draftLaw = "(-1)"; // Set the expression for the extrude
  wallOptions.draftOption = 4; // 4 indicates we use draftlaw
  //Walter - Change the gap type to Extended to get the desired shape
  wallOptions.gapType = SweepOptions.Extended; // I actually don't like this when we have x^2, but it doesn't do much for just x
  //Walter - Create a shell instead of a solid part
  wallOptions.createSolid = true; // This way the shape isn't filled in
  walls.setOptions(wallOptions); // Sets the settings we assigned above

  // Make elliptical pattern for extensions
  var ePattern = new EllipticalPattern();
  ePattern.setCenter(new CoordinateSystemPosition(0, 0, 0));
  ePattern.setNormal(new CoordinateSystemDirection(0, 0, 1));
  ePattern.setInstances(num_ridges);
  ePattern.setRotated(true);

  // Make a recipe for a model
  var wallRecipe = new Recipe();
  wallRecipe.append(walls);
  wallRecipe.append(ePattern);
  var wallModel = new Model();
  wallModel.setRecipe(wallRecipe);
  wallModel.name = "Outer Walls";
  wallModel.getCoordinateSystem().translate(new Cartesian3D(0, 0, 0)); // Makes the model start at the origin

  // Set the material for these parts
  var wallProject = App.getActiveProject()
    .getGeometryAssembly()
    .append(wallModel); // Adds the model to the project
  var pecMaterial = App.getActiveProject().getMaterialList().getMaterial("PEC"); // Makes the material available
  App.getActiveProject().setMaterial(wallProject, pecMaterial); // Sets the material
  //App.getActiveProject().setMaterial( bottom, pecMaterial );						// Sets the material
}
