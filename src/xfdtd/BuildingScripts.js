// This file consolidates all of the antenna building scripts from the GENETIS_PUEO/XMacros directory
// Each individual script is separated by a line of underscores (_______...)
// The original file name is found underneath the first underscore line enclosing the script

// ______________________________________________________________________________________________________________________________________________________________________________________________________________
// buildRidges.js

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
function build_ridges(x_0, y_0, z_0, x_f, y_f, z_f, tau, beta, S, m)
{

	// Curves (Z is logarithmic in t)
	var Log1 = new LawEdge( ""+x_0+" + ("+z_f+"-"+x_0+")/"+tau+"*u", ""+y_0+" + ("+y_f+"-"+y_0+")/"+tau+"*u", ""+beta+"*ln((exp("+z_f+"/"+beta+")-1.0)/"+tau+"*u+1.0)", 0, tau); 
	var Log2 = new LawEdge( ""+x_0+" + ("+z_f+"-"+x_0+")/"+tau+"*u", "-"+y_0+" - ("+y_f+"-"+y_0+")/"+tau+"*u", ""+beta+"*ln((exp("+z_f+"/"+beta+")-1.0)/"+tau+"*u+1.0)", 0, tau);

	// Inner straight slopes 
	var IS1 = new LawEdge( ""+x_0+" + ("+z_f+"-"+x_0+")/"+tau+"*u", ""+y_0+" + ("+y_f+"-"+y_0+")/"+tau+"*u", "("+z_f+"-"+z_0+")/"+tau+"*u", 0, tau); 
	var IS2 = new LawEdge( ""+x_0+" + ("+z_f+"-"+x_0+")/"+tau+"*u", "-"+y_0+" - ("+y_f+"-"+y_0+")/"+tau+"*u", "("+z_f+"-"+z_0+")/"+tau+"*u", 0, tau);

	// Bottom line
	var BL1 = new LawEdge(""+x_0+" + ("+x_f+"-"+x_0+")/"+tau+"*u", ""+y_0+"", ""+z_0+"", 0, tau);
	var BL2 = new LawEdge(""+x_0+" + ("+x_f+"-"+x_0+")/"+tau+"*u", "-"+y_0+"", ""+z_0+"", 0, tau);

	// Top line
	var TL1 = new LawEdge(""+z_f+" + "+x_f+"/"+tau+"*u", ""+y_f+"", ""+z_f+"", 0, tau);
	var TL2 = new LawEdge(""+z_f+" + "+x_f+"/"+tau+"*u", "-"+y_f+"", ""+z_f+"", 0, tau);

	// Outer Straight slopes
	var OS1 = new LawEdge( ""+x_f+" + "+z_f+"/"+tau+"*u", ""+y_0+" + ("+y_f+" - "+y_0+")/"+tau+"*u", ""+z_f+"/"+tau+"*u", 0, tau);
	var OS2 = new LawEdge( ""+x_f+" + "+z_f+"/"+tau+"*u", "-"+y_0+" - ("+y_f+" - "+y_0+")/"+tau+"*u", ""+z_f+"/"+tau+"*u", 0, tau);

	// Inner top line
	var ITL = new LawEdge( ""+z_f+"", "-"+y_f+" + 2*"+y_f+"/"+tau+"*u", ""+z_f+"", 0, tau);

	// Outer top line
	var OTL = new LawEdge( ""+x_f+" + "+z_f+"", "-"+y_f+" + 2*"+y_f+"/"+tau+"*u", ""+z_f+"", 0, tau);

	// Inner bottom line
	var IBL = new LawEdge( ""+x_0+"", "-"+y_0+" + 2*"+y_0+"/"+tau+"*u", ""+z_0+"", 0, tau);

	// Outer bottom line
	var OBL = new LawEdge( ""+x_f+"", "-"+y_0+" + 2*"+y_0+"/"+tau+"*u", ""+z_0+"", 0, tau);

	// Make the sketches
	var straightEdge1 = new Sketch(); 	// All straight edges (IS1, BL1, TL1, OS1)
	var straightEdge2 = new Sketch(); 	// All straight edges (IS2, BL2, TL2, OS2)	
	var curvedLog1 = new Sketch(); 		// Logarithmic edge (IS1 and Log1)
	var curvedLog2 = new Sketch(); 		// Logarithmic edge (IS2 and Log2)
	var topRectangle = new Sketch(); 	// Top rectangle
	var bottomRectangle = new Sketch(); // Bottom rectangle

	// Add the edges to the sketches
	straightEdge1.addEdges( [IS1, BL1, TL1, OS1] );	// Inner straight slope
	curvedLog1.addEdges( [IS1, Log1] );				// Right logarithm part
	straightEdge2.addEdges( [IS2, BL2, TL2, OS2] ); 	// Inner straight slope
	curvedLog2.addEdges( [IS2, Log2] );			 	// Left logarithm part
	topRectangle.addEdges( [ITL, OTL, TL1, TL2] );		// Top rectangle
	bottomRectangle.addEdges( [IBL, OBL, BL1, BL2] );	// Bottom Rectangle

	//WALTER - The Elliptical pattern is added as a recipe to the parts
	//In this case the location of the center and direction of the normal are simple, but for more complex scenarios, may need to use more functionality to find them.
	var ePattern = new EllipticalPattern();
	ePattern.setCenter(new CoordinateSystemPosition(0,0,0));
	ePattern.setNormal(new CoordinateSystemDirection(0,0,1));
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

	var pecMaterial = App.getActiveProject().getMaterialList().getMaterial( "PEC" );

	//WALTER - We can loop over all our parts and add them to the project as follows.  You can use similar concepts above.
	models = new Assembly();
	for(var w = 0; w < cov.length; w++)
	{
		var r = new Recipe();
		r.append(cov[w]);
		r.append(ePattern);
		var m = new Model();
		m.setRecipe(r);
		m.name = "Test Surface " + (w+1);
		//WALTER - Seperate array for the models, though we could just get them from the GemoetryAssembly again
		models.append(m);
		App.getActiveProject().setMaterial( m, pecMaterial );

	}

	// Work on the loft
	var vertex_position1 = curvedLog1.getPosition(curvedLog1.getVertexIds()[0]);	
	var vertex_position2 = curvedLog2.getPosition(curvedLog2.getVertexIds()[0]);

	var loft = new Loft(models.at(2).pickFace(new Cartesian3D (0, 0, 0), vertex_position1, 0.5), "0.0", models.at(3).pickFace(new Cartesian3D(0,0,0), vertex_position2, 0.5), "0.0");
	loft.setPart1(models.at(2));
	loft.setPart2(models.at(3));

	var r12 = new Recipe();
	r12.append( loft );
	r12.append(ePattern);
	var m12 = new Model();
	m12.setRecipe( r12 );
	m12.name = "Loft 1";
	models.append(m12);

	//WALTER - append the assembly to the project, then loop over it to assign the material
	var assembly = App.getActiveProject().getGeometryAssembly().append(models);
	for(x = 0; x < assembly.size(); x++)
	{
		Output.println(assembly.at(x));
		App.getActiveProject().setMaterial( assembly.at(x), pecMaterial );
	}

}

// ______________________________________________________________________________________________________________________________________________________________________________________________________________
// buildWalls.js

// Makes the outer walls of the horn antenna
// S is the side length of the bottom of the wall
// m is the coefficient for the linear function the walls extrude according to (currently set to 1)
// H is the final height of the walls
function build_walls(S,m,H) 
{
	// Make the edges to define the square
	var edge1 = Line( new Cartesian3D(-S,-S, 0), new Cartesian3D(-S, S, 0));
	var edge2 = Line( new Cartesian3D(-S, S, 0), new Cartesian3D(S, S, 0));
	var edge3 = Line( new Cartesian3D(S,S, 0), new Cartesian3D(S, -S, 0));
	var edge4 = Line( new Cartesian3D(S,-S, 0), new Cartesian3D(-S, -S, 0));

//	var edge1 = Line( new Cartesian3D(-S,-S, 0), new Cartesian3D(-S, S, 0));
//	var edge2 = Line( new Cartesian3D(-S, S, 0), new Cartesian3D(S/2, S, 0));
//	var diag1 = Line( new Cartesian3D(S/2, S, 0), new Cartesian3D(S, S/2, 0));	
//	var edge3 = Line( new Cartesian3D(S,S/2, 0), new Cartesian3D(S, -S/2, 0));
//	var diag2 = Line( new Cartesian3D(S, -S/2, 0), new Cartesian3D(S/2, -S, 0));	
//	var edge4 = Line( new Cartesian3D(S,-S, 0), new Cartesian3D(-S, -S, 0));

	// Declare sketches to be made from the edges
	var wallSegment = new Sketch();
	var bottomSegment = new Sketch();
	wallSegment.addEdge(edge1);
	wallSegment.addEdge(edge2);
	wallSegment.addEdge(edge3);
	wallSegment.addEdge(edge4);
//	wallSegment.addEdge(diag1);
//	wallSegment.addEdge(diag2);

	bottomSegment.addEdge(edge1);
	bottomSegment.addEdge(edge2);
	bottomSegment.addEdge(edge3);
	bottomSegment.addEdge(edge4);
//	bottomSegment.addEdge(diag1);
//	bottomSegment.addEdge(diag2);

	// Let's start by making the bottom
	var bottomCover = new Cover(bottomSegment);
	var bottomRecipe = new Recipe();
	bottomRecipe.append( bottomCover );
	var bottomModel = new Model();
	bottomModel.setRecipe( bottomRecipe );
	// Add the surface
	//var bottom = App.getActiveProject().getGeometryAssembly().append(bottomModel);
	//bottom.name = "Bottom square";

	// Now we need to extrude the edges to get height
	var walls = new Extrude( wallSegment, H);				// Makes an Extrude
	var wallOptions = walls.getOptions();						// Gives the possible options for 
	// We will use the draft law option to extrude linearly
	wallOptions.draftOption = SweepOptions.DraftLaw;			// allows for draftlaw
	wallOptions.draftLaw = "("+m+"*x)";							// Set the expression for the extrude
	wallOptions.draftOption = 4;								// 4 indicates we use draftlaw
    //Walter - Change the gap type to Extended to get the desired shape
	wallOptions.gapType = SweepOptions.Extended; 				// I actually don't like this when we have x^2, but it doesn't do much for just x
    //Walter - Create a shell instead of a solid part
	wallOptions.createSolid = false;							// This way the shape isn't filled in
	walls.setOptions ( wallOptions );							// Sets the settings we assigned above

	// Make a recipe for a model
	var wallRecipe = new Recipe();
	wallRecipe.append(walls);
	var wallModel = new Model();
	wallModel.setRecipe(wallRecipe);
	wallModel.name = "Outer Walls";
	wallModel.getCoordinateSystem().translate(new Cartesian3D(0,0,0));	// Makes the model start at the origin

	// Set the material for these parts
	var wallProject = App.getActiveProject().getGeometryAssembly().append(wallModel);	// Adds the model to the project
	var pecMaterial = App.getActiveProject().getMaterialList().getMaterial( "PEC" );	// Makes the material available
	App.getActiveProject().setMaterial( wallProject, pecMaterial );						// Sets the material
	//App.getActiveProject().setMaterial( bottom, pecMaterial );						// Sets the material

}

// ______________________________________________________________________________________________________________________________________________________________________________________________________________
// buildWaveguide.js

// Make a waveguide
function build_waveguide(S,x_0,y_0,D) // D for "depdth"
{

	// Make the edges to define the square
	var edge1 = Line( new Cartesian3D(-S,-S, 0), new Cartesian3D(-S, S, 0));
	var edge2 = Line( new Cartesian3D(-S, S, 0), new Cartesian3D(S, S, 0));
	var edge3 = Line( new Cartesian3D(S,S, 0), new Cartesian3D(S, -S, 0));
	var edge4 = Line( new Cartesian3D(S,-S, 0), new Cartesian3D(-S, -S, 0));

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
	bottomRecipe.append( bottomCover );
	var bottomModel = new Model();
	bottomModel.setRecipe( bottomRecipe );
	// Add the surface
	//var bottom = App.getActiveProject().getGeometryAssembly().append(bottomModel);
	//bottom.name = "Bottom square";

	// Now we need to extrude the edges to get height
	var walls = new Extrude( wallSegment, D);				// Makes an Extrude
	var wallOptions = walls.getOptions();						// Gives the possible options for 
	// We will use the draft law option to extrude linearly
	wallOptions.draftOption = SweepOptions.DraftLaw;			// allows for draftlaw
	wallOptions.draftLaw = "(-1)";							// Set the expression for the extrude
	wallOptions.draftOption = 4;								// 4 indicates we use draftlaw
    //Walter - Change the gap type to Extended to get the desired shape
	wallOptions.gapType = SweepOptions.Extended; 				// I actually don't like this when we have x^2, but it doesn't do much for just x
    //Walter - Create a shell instead of a solid part
	wallOptions.createSolid = false;							// This way the shape isn't filled in
	walls.setOptions ( wallOptions );							// Sets the settings we assigned above

	// Make a recipe for a model
	var wallRecipe = new Recipe();
	wallRecipe.append(walls);
	var wallModel = new Model();
	wallModel.setRecipe(wallRecipe);
	wallModel.name = "Outer Walls";
	wallModel.getCoordinateSystem().translate(new Cartesian3D(0,0,0));	// Makes the model start at the origin

	// Set the material for these parts
	var wallProject = App.getActiveProject().getGeometryAssembly().append(wallModel);	// Adds the model to the project
	var pecMaterial = App.getActiveProject().getMaterialList().getMaterial( "PEC" );	// Makes the material available
	App.getActiveProject().setMaterial( wallProject, pecMaterial );						// Sets the material
	//App.getActiveProject().setMaterial( bottom, pecMaterial );						// Sets the material

}

// ______________________________________________________________________________________________________________________________________________________________________________________________________________
// extend_ridges_trapezoid.js

// New extensions but with trapezoid shapes
// We define L as the half length of the minor side of the trapezoid
// We want the trapezoid to be at 45 degrees from the major base, so we 
//	say the height is y0 - L
function extend_ridges_trapezoid(S, x_0, y_0, D, L, th) // D for "depdth", L for "Length"
{


	// Below works for example antenna at l = (x0-y0)/4
	// Make the edges to define the square
	var edge1 = Line( new Cartesian3D(-S  , y_0, 0), new Cartesian3D(-x_0, y_0, 0)); // good
	var diag1 = Line( new Cartesian3D(-x_0, y_0, 0), new Cartesian3D(-x_0 + th, L, 0)); // good
	var edge5 = Line( new Cartesian3D(-x_0 + th, L, 0), new Cartesian3D(-x_0 + th, -L, 0));	// good
	var diag2 = Line( new Cartesian3D(-x_0 + th, -L, 0), new Cartesian3D(-x_0, -y_0, 0)); // good
	var edge3 = Line( new Cartesian3D(-x_0,-y_0, 0), new Cartesian3D(-S, -y_0, 0)); // good
	var edge4 = Line( new Cartesian3D(-S  ,-y_0, 0), new Cartesian3D(-S, y_0, 0)); // good


// For original (45 degree opening) trapezoid\
/*
	// Below works for example antenna at l = (x0-y0)/4
	// Make the edges to define the square
	var edge1 = Line( new Cartesian3D(-S  , y_0, 0), new Cartesian3D(-x_0, y_0, 0)); // good
	var diag1 = Line( new Cartesian3D(-x_0, y_0, 0), new Cartesian3D(-x_0 - L + y_0, L, 0)); // good
	var edge5 = Line( new Cartesian3D(-x_0 - L + y_0, L, 0), new Cartesian3D(-x_0 - L + y_0, -L, 0));	// good
	var diag2 = Line( new Cartesian3D(-x_0 - L + y_0, -L, 0), new Cartesian3D(-x_0, -y_0, 0)); // good
	var edge3 = Line( new Cartesian3D(-x_0,-y_0, 0), new Cartesian3D(-S, -y_0, 0)); // good
	var edge4 = Line( new Cartesian3D(-S  ,-y_0, 0), new Cartesian3D(-S, y_0, 0)); // good
*/
	// NOT S COME ONNNNNNNNNNNNNNNN
/*	var edge1 = Line( new Cartesian3D(-S,-S, 0), new Cartesian3D(-S, S, 0));
	var edge2 = Line( new Cartesian3D(-S, S, 0), new Cartesian3D(S/2, S, 0));
	var diag1 = Line( new Cartesian3D(S/2, S, 0), new Cartesian3D(S, S/2, 0));	
	var edge3 = Line( new Cartesian3D(S,S/2, 0), new Cartesian3D(S, -S/2, 0));
	var diag2 = Line( new Cartesian3D(S, -S/2, 0), new Cartesian3D(S/2, -S, 0));	
	var edge4 = Line( new Cartesian3D(S/2,-S, 0), new Cartesian3D(-S, -S, 0));
*/
/*
	// NOT S COME ONNNNNNNNNNNNNNNN
	var edge1 = Line( new Cartesian3D(-S, y_0, 0), new Cartesian3D(-S+9*S/10, y_0, 0));
	var diag1 = Line( new Cartesian3D(-S+9*S/10, y_0, 0), new Cartesian3D(-x_0, y_0/2, 0));
	var edge2 = Line( new Cartesian3D(-x_0, y_0/2, 0), new Cartesian3D(-x_0, -y_0/2, 0));	
	var diag2 = Line( new Cartesian3D(-x_0,-y_0/2, 0), new Cartesian3D(-S+9*S/10, -y_0, 0));
	var edge3 = Line( new Cartesian3D(-S+9*S/10, -y_0, 0), new Cartesian3D(-S, -y_0, 0));	
	var edge4 = Line( new Cartesian3D(-S,-y_0, 0), new Cartesian3D(-S, y_0, 0));
*/

/*
	// NOT S COME ONNNNNNNNNNNNNNNN
	var edge1 = Line( new Cartesian3D(-S, y_0, 0), new Cartesian3D(-x_0-y_0/2, y_0, 0));
	var diag1 = Line( new Cartesian3D(-x_0-y_0/2, y_0, 0), new Cartesian3D(-x_0, y_0/2, 0));
	var edge2 = Line( new Cartesian3D(-x_0, y_0/2, 0), new Cartesian3D(-x_0, -y_0/2, 0));	
	var diag2 = Line( new Cartesian3D(-x_0,-y_0/2, 0), new Cartesian3D(-x_0-y_0/2, -y_0, 0));
	var edge3 = Line( new Cartesian3D(-x_0-y_0/2, -y_0, 0), new Cartesian3D(-S, -y_0, 0));	
	var edge4 = Line( new Cartesian3D(-S,-y_0, 0), new Cartesian3D(-S, y_0, 0));
*/


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
	bottomRecipe.append( bottomCover );
	var bottomModel = new Model();
	bottomModel.setRecipe( bottomRecipe );
	// Add the surface
	//var bottom = App.getActiveProject().getGeometryAssembly().append(bottomModel);
	//bottom.name = "Bottom square";

	// Now we need to extrude the edges to get height
	var walls = new Extrude( wallSegment, D);				// Makes an Extrude
	var wallOptions = walls.getOptions();						// Gives the possible options for 
	// We will use the draft law option to extrude linearly
	wallOptions.draftOption = SweepOptions.DraftLaw;			// allows for draftlaw
	wallOptions.draftLaw = "(-1)";							// Set the expression for the extrude
	wallOptions.draftOption = 4;								// 4 indicates we use draftlaw
    //Walter - Change the gap type to Extended to get the desired shape
	wallOptions.gapType = SweepOptions.Extended; 				// I actually don't like this when we have x^2, but it doesn't do much for just x
    //Walter - Create a shell instead of a solid part
	wallOptions.createSolid = true;							// This way the shape isn't filled in
	walls.setOptions ( wallOptions );							// Sets the settings we assigned above

	// Make elliptical pattern for extensions
	var ePattern = new EllipticalPattern();
	ePattern.setCenter(new CoordinateSystemPosition(0,0,0));
	ePattern.setNormal(new CoordinateSystemDirection(0,0,1));
	ePattern.setInstances(num_ridges);
	ePattern.setRotated(true);

	// Make a recipe for a model
	var wallRecipe = new Recipe();
	wallRecipe.append(walls);
	wallRecipe.append(ePattern);
	var wallModel = new Model();
	wallModel.setRecipe(wallRecipe);
	wallModel.name = "Outer Walls";
	wallModel.getCoordinateSystem().translate(new Cartesian3D(0,0,0));	// Makes the model start at the origin

	// Set the material for these parts
	var wallProject = App.getActiveProject().getGeometryAssembly().append(wallModel);	// Adds the model to the project
	var pecMaterial = App.getActiveProject().getMaterialList().getMaterial( "PEC" );	// Makes the material available
	App.getActiveProject().setMaterial( wallProject, pecMaterial );						// Sets the material
	//App.getActiveProject().setMaterial( bottom, pecMaterial );						// Sets the material

}


// ______________________________________________________________________________________________________________________________________________________________________________________________________________
// CreateAntennaSource.js

function CreateAntennaSource(h_or_v, x, y, Height, L)
{
    // Here we will create our waveform, create our circuit component definition for the feed, and create
    // a CircuitComponent that will attach those to our current geometry.
    var waveformList = App.getActiveProject().getWaveformList();
        // clear the waveform list
	    waveformList.clear();

    // Create a gaussian derivative input wave
    var waveform = new Waveform();
    var GDer = new GaussianDerivativeWaveformShape ();
    GDer.pulseWidth = 2e-9;
    waveform.setWaveformShape( GDer );
    waveform.name ="Gaussian Derivative";
    var waveformInList = waveformList.addWaveform( waveform );

    // Now to create the circuit component definition:
    var componentDefinitionList = App.getActiveProject().getCircuitComponentDefinitionList();
    // clear the list
    componentDefinitionList.clear();

    // Create our Feed
    var feed1 = new Feed();
    var feed2 = new Feed();

    feed1.feedType = Feed.Voltage; // Set its type enumeration to be Voltage.
    //feed2.feedType = Feed.Voltage; // Set its type enumeration to be Voltage.

    // Define a 50-ohm resistance for this feed
    var rlc = new RLCSpecification();
    rlc.setResistance( "50 ohm" );
    rlc.setCapacitance( "0" );
    rlc.setInductance( "0" );
    feed1.setImpedanceSpecification( rlc );
    feed1.setWaveform( waveformInList );  // Make sure to use the reference that was returned by the list, or query the list directly
    feed1.name = "50-Ohm Voltage Source";
    var feedInList = componentDefinitionList.addCircuitComponentDefinition( feed1 );


	feed2.setImpedanceSpecification( rlc );
    feed2.setWaveform( waveformInList );  // Make sure to use the reference that was returned by the list, or query the list directly
    feed2.name = "50-Ohm Voltage Source 2";
    var feedInList = componentDefinitionList.addCircuitComponentDefinition( feed2 );

    // Now create a circuit component that will be the feed point for our simulation
    var componentList = App.getActiveProject().getCircuitComponentList();
    componentList.clear();

    var component1 = new CircuitComponent();
	//var component2 = new CircuitComponent();

	component1.name = "Source";
	//component2.name = "Source";

    component1.setAsPort( true );
    //component2.setAsPort( true );
    // Define the endpoints of this feed - these are defined in world position, but you can also attach them to edges, faces, etc.
/*	if(h_or_v == 0) // 0 for h, 1 for v
	{
		var coordinate1 = new CoordinateSystemPosition( -x - L + y, 0, Height);
		var coordinate2 = new CoordinateSystemPosition( x + L - y, 0, Height);
	}
	else
	{
		var coordinate1 = new CoordinateSystemPosition( 0, -x - L + y, Height);
    	var coordinate2 = new CoordinateSystemPosition( 0, x + L - y, Height);
		
	}
*/
	if(h_or_v == 0) // 0 for h, 1 for v
	{
		var coordinate1 = new CoordinateSystemPosition( -x, 0, Height);
		var coordinate2 = new CoordinateSystemPosition( x, 0, Height);
	}
	else
	{
		var coordinate1 = new CoordinateSystemPosition( 0, -x, Height);
    	var coordinate2 = new CoordinateSystemPosition( 0, x, Height);

	}
	//var coordinate3 = new CoordinateSystemPosition( 0, -x2, height);
    //var coordinate4 = new CoordinateSystemPosition( 0, x2, height);
    component1.setCircuitComponentDefinition( feed1 );
    component1.setCircuitComponentDefinition( feed1 );
    component1.setEndpoint1( coordinate1 );
    component1.setEndpoint2( coordinate2 );
/*
    component2.setCircuitComponentDefinition( feed2 );
    component2.setCircuitComponentDefinition( feed2 );
    component2.setEndpoint1( coordinate3 );
    component2.setEndpoint2( coordinate4 );
*/
    componentList.addCircuitComponent( component1 );
    //componentList.addCircuitComponent( component2 );

}

// ______________________________________________________________________________________________________________________________________________________________________________________________________________
