/**
 * Grafo.js
 * Carga un grafo de escena en Threejs y lo visualiza
 *
 */

var renderer, scene, camera;

var planta;

var puntuacion;

var force=1;

const L = 500;

var fase = 1;

var disparo = false;

var supervivientes = [0,0,0,0,0,0,0,0,0,0];

var puntos = 0;

var bola, bolaBody, reloj,suelo, ground;

var bolos1, bolos2, bolos3, bolos4, bolos5, bolos6, bolos7, bolos8, bolos9, bolos10;
var bolo1Body, bolo2Body, bolo3Body, bolo4Body, bolo5Body, bolo6Body, bolo7Body, bolo8Body, bolo9Body, bolo10Body;

var booleana;

var gui, sub;

var cameraControls;

initPhysicWorld();
init();
loadScene();
setupGUI();
render();

function init() {
    //Inicializar Threejs
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0x0000AA));
    //renderer.shadowMap.enabled = true;
    renderer.autoClear = false;
    document.getElementById('container').appendChild(renderer.domElement);

    	// Reloj
	  reloj = new THREE.Clock();
	  reloj.start();
    scene = new THREE.Scene();

    setCameras(window.innerWidth/window.innerHeight);
    
    cameraControls = new THREE.OrbitControls(camera, renderer.domElement);
    cameraControls.target.set(0,110,0);

    //Luces
    var ambiental = new THREE.AmbientLight(0x444444);
    scene.add(ambiental);

    var puntual = new THREE.PointLight('yellow', 0.3);
    puntual.position.y = 200;
    scene.add(puntual);

    var focal = new THREE.SpotLight('white', 0.5);
    focal.position.set(300, 600, -800);
    focal.target.position.set(0,0,0);
    focal.angle = Math.PI / 7;
    focal.penumbra = 1;

    focal.shadow.camera.near = 30;
    focal.shadow.camera.far = 1500;
    focal.shadow.camera.fov = 40000;
    focal.shadow.mapSize.width = 1024000;
    focal.shadow.mapSize.height = 1024000;

    scene.add(focal.target);
    
    focal.castShadow = true;
    scene.add(focal);

    cameraControls.noKeys = true;
    
    window.addEventListener('resize', updateAspectRatio);

}

function setCameras(ar){
  var camaraOrtografica;

  if(ar<1){
    camaraOrtografica = new THREE.OrthographicCamera( -L, L, L/ar, -L/ar, -1, 100000);
  }
  else{
    camaraOrtografica = new THREE.OrthographicCamera( -L*ar, L*ar, L, -L, -1, 100000);
  }

  camaraOrtografica.lookAt(new THREE.Vector3(0, 0, 0));

  planta = camaraOrtografica.clone();
  planta.position.set(0,L,0);
  planta.up = new THREE.Vector3(0,0,-1);
  planta.lookAt(new THREE.Vector3(0, 0, 0));

  var camaraPerspectiva = new THREE.PerspectiveCamera(75, ar, 0.1, 100000);
  camaraPerspectiva.position.set(0,400,800);
  camaraPerspectiva.lookAt(new THREE.Vector3(0,110,0));

  camera = camaraPerspectiva.clone();

  scene.add(camera);
  scene.add(planta);
}

function loadScene() {
    //Carga la escena
  
    //Puntuacion
    var matTexto = new THREE.MeshPhongMaterial({color:'yellow', wireframe:false});
    var str1 = "La puntuacion actual es "
    var str2 = puntos.toString();
    var mensaje = str1.concat(str2);
    var textLoader = new THREE.FontLoader();
    textLoader.load('fonts/helvetiker_regular.typeface.json', 
    function(font){var geoPuntuacion = new THREE.TextGeometry(mensaje,
                  {size: 1,height: 0.1,curveSegments: 3, font:font,weight: "bold",style: "normal",bevelThickness: 0.05,bevelSize: 0.04,bevelEnable: true});
                  puntuacion = new THREE.Mesh(geoPuntuacion, matTexto);
                  scene.add(puntuacion);
                  puntuacion.position.set(-400,400,1);
                  puntuacion.scale.set(50,50,50);});
    
    //Texturas
    var path = "images/";
    var txSuelo = new THREE.TextureLoader().load(path + "pista_bowl.jpg");
    var matSuelo = new THREE.MeshLambertMaterial({color:'white', wireframe:false, map:txSuelo});
    var txBolo = new THREE.TextureLoader().load(path + "bowltx.jpg");
    var txBola = new THREE.TextureLoader().load(path + "metal_128.jpg");

    var paredes = [path + "posx.jpg", path + "negx.jpg", path + "posy.jpg", path + "negy.jpg", path + "posz.jpg", path + "negz.jpg"];

    var mapaEntorno = new THREE.CubeTextureLoader().load(paredes);
  
    //Habitación

    var shader = THREE.ShaderLib.cube;
    shader.uniforms.tCube.value = mapaEntorno;

    var matParedes = new THREE.ShaderMaterial(
        {
            fragmentShader: shader.fragmentShader,
            vertexShader: shader.vertexShader,
            uniforms: shader.uniforms,
            depthWrite: false,
            side: THREE.BackSide
        }
    );

    var habitacion = new THREE.Mesh(new THREE.BoxGeometry(2000,2000,2000), matParedes);
    scene.add(habitacion);
    
    //Modelo de los bolos
    matBolos = new THREE.MeshPhongMaterial({color:'white', wireframe:false, map:txBolo});
    geoBolos = new THREE.CylinderGeometry(0, 30, 140, 20);

    bolos1 = new THREE.Mesh(geoBolos, matBolos);
    bolos1.position.copy(bolo1Body.position);
    bolos1.quaternion.copy(bolo1Body.quaternion);
    bolos1.castShadow = true;
    bolos1.receiveShadow = true;
    scene.add(bolos1);

    bolos2 = new THREE.Mesh(geoBolos, matBolos);
    bolos2.position.copy(bolo2Body.position);
    bolos2.quaternion.copy(bolo2Body.quaternion);
    bolos2.castShadow = true;
    bolos2.receiveShadow = true;
    scene.add(bolos2);

    bolos3 = new THREE.Mesh(geoBolos, matBolos);
    bolos3.position.copy(bolo3Body.position);
    bolos3.quaternion.copy(bolo3Body.quaternion);
    bolos3.castShadow = true;
    bolos3.receiveShadow = true;
    scene.add(bolos3);

    bolos4 = new THREE.Mesh(geoBolos, matBolos);
    bolos4.position.copy(bolo4Body.position);
    bolos4.quaternion.copy(bolo4Body.quaternion);
    bolos4.castShadow = true;
    bolos4.receiveShadow = true;
    scene.add(bolos4);

    bolos5 = new THREE.Mesh(geoBolos, matBolos);
    bolos5.position.copy(bolo5Body.position);
    bolos5.quaternion.copy(bolo5Body.quaternion);
    bolos5.castShadow = true;
    bolos5.receiveShadow = true;
    scene.add(bolos5);

    bolos6 = new THREE.Mesh(geoBolos, matBolos);
    bolos6.position.copy(bolo6Body.position);
    bolos6.quaternion.copy(bolo6Body.quaternion);
    bolos6.castShadow = true;
    bolos6.receiveShadow = true;
    scene.add(bolos6);

    bolos7 = new THREE.Mesh(geoBolos, matBolos);
    bolos7.position.copy(bolo7Body.position);
    bolos7.quaternion.copy(bolo7Body.quaternion);
    bolos7.castShadow = true;
    bolos7.receiveShadow = true;
    scene.add(bolos7);

    bolos8 = new THREE.Mesh(geoBolos, matBolos);
    bolos8.position.copy(bolo8Body.position);
    bolos8.quaternion.copy(bolo8Body.quaternion);
    bolos8.castShadow = true;
    bolos8.receiveShadow = true;
    scene.add(bolos8);

    bolos9 = new THREE.Mesh(geoBolos, matBolos);
    bolos9.position.copy(bolo9Body.position);
    bolos9.quaternion.copy(bolo9Body.quaternion);
    bolos9.castShadow = true;
    bolos9.receiveShadow = true;
    scene.add(bolos9);

    bolos10 = new THREE.Mesh(geoBolos, matBolos);
    bolos10.position.copy(bolo10Body.position);
    bolos10.quaternion.copy(bolo10Body.quaternion);
    bolos10.castShadow = true;
    bolos10.receiveShadow = true;
    scene.add(bolos10);

    //Modelo de la bola

    matBola = new THREE.MeshPhongMaterial({color:'green', wireframe:false, map:txBola});
    geoBola = new THREE.SphereGeometry(25, 250, 250);
    
    bola = new THREE.Mesh(geoBola, matBola);

    bola.position.copy(bolaBody.position);
    bola.quaternion.copy(bolaBody.quaternion);
    bola.receiveShadow = true;
    bola.castShadow = true;
    scene.add(bola);

    //Añadimos un suelo
    var geoSuelo = new THREE.PlaneGeometry(2000, 2000, 15, 15);
    suelo = new THREE.Mesh(geoSuelo, matSuelo);
    suelo.position.copy(ground.position);
    suelo.quaternion.copy(ground.quaternion);
    suelo.receiveShadow = true;
    scene.add(suelo);
    
    var keyboard = new THREEx.KeyboardState(renderer.domElement);
    renderer.domElement.setAttribute("tabIndex", "0");
    renderer.domElement.focus();

    keyboard.domElement.addEventListener('keydown', function(event){
      if(keyboard.eventMatches(event, 'left') && !disparo){bolaBody.position.x -= 10;}
      if(keyboard.eventMatches(event, 'right') && !disparo){bolaBody.position.x += 10;}
      if(keyboard.eventMatches(event, 'up')){
        disparo = true;
        derribados = [0,0,0,0,0,0,0,0,0,0];
        bolaBody.velocity = new CANNON.Vec3(0,0,-2000*force);
        if(fase==1){
          setTimeout(function(){
            i = 30;
            if(bolo1Body.position.x>20+i || bolo1Body.position.x<20-i || bolo1Body.position.z>-330+i || bolo1Body.position.z<-330-i){derribados[0]+=1;}
            if(bolo2Body.position.x>50+i || bolo2Body.position.x<50-i || bolo2Body.position.z>-400+i || bolo2Body.position.z<-400-i){derribados[1]+=1;}
            if(bolo3Body.position.x>-10+i || bolo3Body.position.x<-10-i || bolo3Body.position.z>-400+i || bolo3Body.position.z<-400-i){derribados[2]+=1;}
            if(bolo4Body.position.x>80+i || bolo4Body.position.x<80-i || bolo4Body.position.z>-470+i || bolo4Body.position.z<-470-i){derribados[3]+=1;}
            if(bolo5Body.position.x>20+i || bolo5Body.position.x<20-i || bolo5Body.position.z>-470+i || bolo5Body.position.z<-470-i){derribados[4]+=1;}
            if(bolo6Body.position.x>-40+i || bolo6Body.position.x<-40-i || bolo6Body.position.z>-470+i || bolo6Body.position.z<-470-i){derribados[5]+=1;}
            if(bolo7Body.position.x>110+i || bolo7Body.position.x<110-i || bolo7Body.position.z>-540+i || bolo7Body.position.z<-540-i){derribados[6]+=1;}
            if(bolo8Body.position.x>50+i || bolo8Body.position.x<50-i || bolo8Body.position.z>-540+i || bolo8Body.position.z<-540-i){derribados[7]+=1;}
            if(bolo9Body.position.x>-10+i || bolo9Body.position.x<-10-i || bolo9Body.position.z>-540+i || bolo9Body.position.z<-540-i){derribados[8]+=1;}
            if(bolo10Body.position.x>-70+i || bolo10Body.position.x<-70-i || bolo10Body.position.z>-540+i || bolo10Body.position.z<-540-i){derribados[9]+=1;}
            fase = 2;
          },5000);
        }
        else if(fase==3){
            setTimeout(function(){
            i = 30;
            if(supervivientes[0]==1){if(bolo1Body.position.x>20+i || bolo1Body.position.x<20-i || bolo1Body.position.z>-330+i || bolo1Body.position.z<-330-i){derribados[0]+=1;}}
            if(supervivientes[1]==1){if(bolo2Body.position.x>50+i || bolo2Body.position.x<50-i || bolo2Body.position.z>-400+i || bolo2Body.position.z<-400-i){derribados[1]+=1;}}
            if(supervivientes[2]==1){if(bolo3Body.position.x>-10+i || bolo3Body.position.x<-10-i || bolo3Body.position.z>-400+i || bolo3Body.position.z<-400-i){derribados[2]+=1;}}
            if(supervivientes[3]==1){if(bolo4Body.position.x>80+i || bolo4Body.position.x<80-i || bolo4Body.position.z>-470+i || bolo4Body.position.z<-470-i){derribados[3]+=1;}}
            if(supervivientes[4]==1){if(bolo5Body.position.x>20+i || bolo5Body.position.x<20-i || bolo5Body.position.z>-470+i || bolo5Body.position.z<-470-i){derribados[4]+=1;}}
            if(supervivientes[5]==1){if(bolo6Body.position.x>-40+i || bolo6Body.position.x<-40-i || bolo6Body.position.z>-470+i || bolo6Body.position.z<-470-i){derribados[5]+=1;}}
            if(supervivientes[6]==1){if(bolo7Body.position.x>110+i || bolo7Body.position.x<110-i || bolo7Body.position.z>-540+i || bolo7Body.position.z<-540-i){derribados[6]+=1;}}
            if(supervivientes[7]==1){if(bolo8Body.position.x>50+i || bolo8Body.position.x<50-i || bolo8Body.position.z>-540+i || bolo8Body.position.z<-540-i){derribados[7]+=1;}}
            if(supervivientes[8]==1){if(bolo9Body.position.x>-10+i || bolo9Body.position.x<-10-i || bolo9Body.position.z>-540+i || bolo9Body.position.z<-540-i){derribados[8]+=1;}}
            if(supervivientes[9]==1){if(bolo10Body.position.x>-70+i || bolo10Body.position.x<-70-i || bolo10Body.position.z>-540+i || bolo10Body.position.z<-540-i){derribados[9]+=1;}}
            fase = 4; 
            },5000);
        }
      }
    }
    );
}   

function setupGUI(){
    //Construye la interfaz de usuario
    effectControl = {
      instr1: "- Mueva la bola con las flechas",
      instr2: "  izquierda y derecha.", 
      instr3: "- En 'Control Bola', ajuste la", 
      instr4: "  fuerza de disparo de la bola.", 
      instr5: "- Para lanzar la bola, pulse la flecha ",
      instr6: "  arriba.",
      fuerza: 1
    };
    
    gui = new dat.GUI({autoPlace: true, width: 400});

    pestaña1 = gui.addFolder("Control Bola");
    pestaña2 = gui.addFolder("Instrucciones");
    pestaña1.add(effectControl, "fuerza", 1.0, 10.0, 1).name("Fuerza de la bola").onChange(function(value){
      force = effectControl.fuerza;
    });
    pestaña2.add(effectControl, "instr1"); pestaña2.add(effectControl, "instr2"); pestaña2.add(effectControl, "instr3"); pestaña2.add(effectControl, "instr4"); pestaña2.add(effectControl, "instr5"); pestaña2.add(effectControl, "instr6");
}

function updateAspectRatio(){
  //Ajustar la cámara y el viewport a las nuevas dimensiones del canvas
  renderer.setSize(window.innerWidth, window.innerHeight);
  var aspectRatio = window.innerWidth/window.innerHeight;

  camera.aspect = aspectRatio;
  camera.updateProjectionMatrix();
}

function update()
{
  
  var segundos = reloj.getDelta();	// tiempo en segundos que ha pasado
  world.step( segundos );				// recalcula el mundo tras ese tiempo
  
  
  suelo.position.x = ground.position.x;
  suelo.position.y = ground.position.y-60;
  suelo.position.z = ground.position.z;
  suelo.quaternion.copy(ground.quaternion);

  bola.position.copy(bolaBody.position);
  bola.quaternion.copy(bolaBody.quaternion);
  
  bolos1.position.copy(bolo1Body.position);
  bolos1.quaternion.copy(bolo1Body.quaternion);

  bolos2.position.copy(bolo2Body.position);
  bolos2.quaternion.copy(bolo2Body.quaternion);

  bolos3.position.copy(bolo3Body.position);
  bolos3.quaternion.copy(bolo3Body.quaternion);

  bolos4.position.copy(bolo4Body.position);
  bolos4.quaternion.copy(bolo4Body.quaternion);

  bolos5.position.copy(bolo5Body.position);
  bolos5.quaternion.copy(bolo5Body.quaternion);

  bolos6.position.copy(bolo6Body.position);
  bolos6.quaternion.copy(bolo6Body.quaternion);

  bolos7.position.copy(bolo7Body.position);
  bolos7.quaternion.copy(bolo7Body.quaternion);

  bolos8.position.copy(bolo8Body.position);
  bolos8.quaternion.copy(bolo8Body.quaternion);

  bolos9.position.copy(bolo9Body.position);
  bolos9.quaternion.copy(bolo9Body.quaternion);

  bolos10.position.copy(bolo10Body.position);
  bolos10.quaternion.copy(bolo10Body.quaternion);

  if(fase==2){
    if(derribados[0]==1){
      bolo1Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[0]+=1;
    }
    if(derribados[1]==1){
      bolo1Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[1]+=1;
    }
    if(derribados[2]==1){
      bolo3Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[2]+=1;
    }
    if(derribados[3]==1){
      bolo4Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[3]+=1;
    }
    if(derribados[4]==1){
      bolo5Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[4]+=1;
    }
    if(derribados[5]==1){
      bolo6Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[5]+=1;
    }
    if(derribados[6]==1){
      bolo7Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[6]+=1;
    }
    if(derribados[7]==1){
      bolo8Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[7]+=1;
    }
    if(derribados[8]==1){
      bolo9Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[8]+=1;
    }
    if(derribados[9]==1){
      bolo10Body.position.x = 10000; puntos +=1;
    } else{
      supervivientes[9]+=1;
    }
    bolaBody.velocity.set(0,0,0);
    bolaBody.position.set(21,20,400);
    disparo = false;
    if(puntos==10){
      scene.remove(puntuacion);
      var matTexto = new THREE.MeshPhongMaterial({color:'yellow', wireframe:false});
      var mensaje = "¡PLENO!"
      var textLoader = new THREE.FontLoader();
      textLoader.load('fonts/helvetiker_regular.typeface.json', 
      function(font){var geoPuntuacion = new THREE.TextGeometry(mensaje,
                    {size: 1,height: 0.1,curveSegments: 3, font:font,weight: "bold",style: "normal",bevelThickness: 0.05,bevelSize: 0.04,bevelEnable: true});
                    puntuacion = new THREE.Mesh(geoPuntuacion, matTexto);
                    scene.add(puntuacion);
                    puntuacion.position.set(-400,400,1);
                    puntuacion.scale.set(50,50,50);});
      fase = 1;
    }
    else {
      fase = 3;
      scene.remove(puntuacion);
      var matTexto = new THREE.MeshPhongMaterial({color:'yellow', wireframe:false});
      var str1 = "La puntuacion actual es "
      var str2 = puntos.toString();
      var mensaje = str1.concat(str2);
      var textLoader = new THREE.FontLoader();
      textLoader.load('fonts/helvetiker_regular.typeface.json', 
      function(font){var geoPuntuacion = new THREE.TextGeometry(mensaje,
                    {size: 1,height: 0.1,curveSegments: 3, font:font,weight: "bold",style: "normal",bevelThickness: 0.05,bevelSize: 0.04,bevelEnable: true});
                    puntuacion = new THREE.Mesh(geoPuntuacion, matTexto);
                    scene.add(puntuacion);
                    puntuacion.position.set(-400,400,1);
                    puntuacion.scale.set(50,50,50);});
    }
  }

  if(fase==4){
    bolo1Body.position.set(20,90,-330);
    bolo2Body.position.set(50,90,-400); 
    bolo3Body.position.set(-10,90,-400); 
    bolo4Body.position.set(80,90,-470); 
    bolo5Body.position.set(20,90,-470); 
    bolo6Body.position.set(-40,90,-470); 
    bolo7Body.position.set(110,90,-540); 
    bolo8Body.position.set(50,90,-540); 
    bolo9Body.position.set(-10,90,-540); 
    bolo10Body.position.set(-70,90,-540);
    
    bolaBody.velocity.set(0,0,0);
    bolaBody.position.set(21,20,400);

    disparo = false;
    if(puntos==10){
      scene.remove(puntuacion);
      var matTexto = new THREE.MeshPhongMaterial({color:'yellow', wireframe:false});
      var mensaje = "¡SEMIPLENO!"
      var textLoader = new THREE.FontLoader();
      textLoader.load('fonts/helvetiker_regular.typeface.json', 
      function(font){var geoPuntuacion = new THREE.TextGeometry(mensaje,
                    {size: 1,height: 0.1,curveSegments: 3, font:font,weight: "bold",style: "normal",bevelThickness: 0.05,bevelSize: 0.04,bevelEnable: true});
                    puntuacion = new THREE.Mesh(geoPuntuacion, matTexto);
                    scene.add(puntuacion);
                    puntuacion.position.set(-400,400,1);
                    puntuacion.scale.set(50,50,50);});
      fase = 1;
    }
    else {
      fase = 1; 
      puntos = 0;
      scene.remove(puntuacion);
      var matTexto = new THREE.MeshPhongMaterial({color:'yellow', wireframe:false});
      var str1 = "La puntuacion actual es "
      var str2 = puntos.toString();
      var mensaje = str1.concat(str2);
      var textLoader = new THREE.FontLoader();
      textLoader.load('fonts/helvetiker_regular.typeface.json', 
      function(font){var geoPuntuacion = new THREE.TextGeometry(mensaje,
                    {size: 1,height: 0.1,curveSegments: 3, font:font,weight: "bold",style: "normal",bevelThickness: 0.05,bevelSize: 0.04,bevelEnable: true});
                    puntuacion = new THREE.Mesh(geoPuntuacion, matTexto);
                    scene.add(puntuacion);
                    puntuacion.position.set(-400,400,1);
                    puntuacion.scale.set(50,50,50);});
    }
  }
}

function render(){
    requestAnimationFrame(render);
    renderer.domElement.setAttribute("tabIndex", "0");
    renderer.domElement.focus();
    update();
    renderer.clear();

    renderer.setViewport(0, 0, window.innerWidth, window.innerHeight);
    renderer.render(scene, camera);
    
    aspectRatio = window.innerWidth/window.innerHeight;
    if(aspectRatio<1){
      renderer.setViewport(0, 0, window.innerWidth/4, window.innerWidth/4);
    }
    else{
      renderer.setViewport(0, 0, window.innerHeight/4, window.innerHeight/4);
    }
    renderer.render(scene, planta);

}

function initPhysicWorld()
{
	// Mundo 
  	world = new CANNON.World(); 
   	world.gravity.set(0,-9.8, 0); 
   	///world.broadphase = new CANNON.NaiveBroadphase(); 
   	world.solver.iterations = 10; 

   	// Material y comportamiento
    var groundMaterial = new CANNON.Material("groundMaterial");
    var materialEsfera = new CANNON.Material("sphereMaterial");
    var materialBolo = new CANNON.Material("cylinderMaterial");
    world.addMaterial( materialEsfera );
    world.addMaterial( materialBolo );
    world.addMaterial( groundMaterial );
    // -existe un defaultContactMaterial con valores de restitucion y friccion por defecto
    // -en caso que el material tenga su friccion y restitucion positivas, estas prevalecen 
    var sphereGroundContactMaterial = new CANNON.ContactMaterial(groundMaterial,materialEsfera,
    										    				{ friction: 0.3, 
                                        restitution: 0 });
    var bowlGroundContactMaterial = new CANNON.ContactMaterial(materialBolo,groundMaterial,
                                    { friction: 0.3, 
                                        restitution: 0 });
    var bowlSphereContactMaterial = new CANNON.ContactMaterial(materialEsfera,materialBolo,
                                    { friction: 0.3, 
                                        restitution: 0,
                                        contactEquationStiffness: 100 });
    var bowlBowlContactMaterial = new CANNON.ContactMaterial(materialBolo,materialBolo,
                                    { friction: 0, 
                                        restitution: 0,
                                        contactEquationStiffness: 0 });
    world.addContactMaterial(sphereGroundContactMaterial);
    world.addContactMaterial(bowlGroundContactMaterial);
    world.addContactMaterial(bowlSphereContactMaterial);
    world.addContactMaterial(bowlBowlContactMaterial);

    bolaBody = new CANNON.Body({mass:850,material:world.materials[0]});
    bolaBody.addShape(new CANNON.Sphere(25));
    bolaBody.position.set(21,20,400);
    world.addBody(bolaBody);
    
    bolo1Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo1Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo1Body.position.set(20,90,-330);
    world.addBody(bolo1Body);

    bolo2Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo2Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo2Body.position.set(50,90,-400);
    world.addBody(bolo2Body);

    bolo3Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo3Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo3Body.position.set(-10,90,-400);
    world.addBody(bolo3Body);

    bolo4Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo4Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo4Body.position.set(80,90,-470);
    world.addBody(bolo4Body);

    bolo5Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo5Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo5Body.position.set(20,90,-470);
    world.addBody(bolo5Body);

    bolo6Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo6Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo6Body.position.set(-40,90,-470);
    world.addBody(bolo6Body);

    bolo7Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo7Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo7Body.position.set(110,90,-540);
    world.addBody(bolo7Body);

    bolo8Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo8Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo8Body.position.set(50,90,-540);
    world.addBody(bolo8Body);

    bolo9Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo9Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo9Body.position.set(-10,90,-540);
    world.addBody(bolo9Body);

    bolo10Body  = new CANNON.Body({mass:200,material:world.materials[1]});
    bolo10Body.addShape(new CANNON.Cylinder(0, 30, 140, 20));
    bolo10Body.position.set(-70,90,-540);
    world.addBody(bolo10Body);

    // Suelo
    var groundShape = new CANNON.Plane();
    ground = new CANNON.Body({ mass: 0, material: groundMaterial });
    ground.addShape(groundShape);
    ground.quaternion.setFromAxisAngle(new CANNON.Vec3(1,0,0),-Math.PI/2);
    world.addBody(ground);
}

