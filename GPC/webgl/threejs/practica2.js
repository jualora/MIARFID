/**
 * Grafo.js
 * Carga un grafo de escena en Threejs y lo visualiza
 *
 */

var renderer, scene, camera;

var angulo = 0;
var cuboEsfera;

init();
loadScene();
render();

function init() {
    //Inicializar Threejs
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0x0000AA));
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);

    camera.position.set(90, 300, 250);
    camera.lookAt(new THREE.Vector3(0,0,0));

}

function loadScene() {
    //Carga la escena
    var matRobot = new THREE.MeshBasicMaterial({color:'red', wireframe: true});
    var geoBaseRobot = new THREE.CylinderGeometry(50, 50, 15, 32);
    var geoEje = new THREE.CylinderGeometry(20, 20, 18, 32);
    var geoEsparrago = new THREE.BoxGeometry(18, 120, 12);
    var geoRotula = new THREE.SphereGeometry(20, 30, 15);
    var geoDisco = new THREE.CylinderGeometry(22, 22, 6, 32);
    var geoNervios = new THREE.BoxGeometry(4,80,4);
    var geoMano = new THREE.CylinderGeometry(15, 15, 40, 32);
    var geoPinza = new THREE.Geometry();
    geoPinza.vertices.push(
        new THREE.Vector3(0, -8, -10), //0
        new THREE.Vector3(19, -8, -10), //1
        new THREE.Vector3(0, -8, 10), //2
        new THREE.Vector3(19, -8, 10), //3
        new THREE.Vector3(0, -12, -10), //4
        new THREE.Vector3(19, -12, -10), //5
        new THREE.Vector3(0, -12, 10), //6
        new THREE.Vector3(19, -12, 10), //7
        new THREE.Vector3(38, -8, -5), //8
        new THREE.Vector3(38, -12, -5), //9
        new THREE.Vector3(38, -8, 5), //10
        new THREE.Vector3(38, -12, 5), //11
    );
    geoPinza.faces.push(
        new THREE.Face3(0, 3, 2),
        new THREE.Face3(0, 1, 3),
        new THREE.Face3(1, 7, 3),
        new THREE.Face3(1, 5, 7),
        new THREE.Face3(5, 6, 7),
        new THREE.Face3(5, 4, 6),
        new THREE.Face3(4, 2, 6),
        new THREE.Face3(4, 0, 2),
        new THREE.Face3(2, 7, 6),
        new THREE.Face3(2, 3, 7),
        new THREE.Face3(4, 1, 0),
        new THREE.Face3(4, 5, 1),
        new THREE.Face3(1, 10, 3),
        new THREE.Face3(1, 8, 10),
        new THREE.Face3(8, 11, 10),
        new THREE.Face3(8, 9, 11),
        new THREE.Face3(9, 7, 11),
        new THREE.Face3(9, 5, 7),
        new THREE.Face3(3, 11, 7),
        new THREE.Face3(3, 10, 11),
        new THREE.Face3(5, 8, 1),
        new THREE.Face3(5, 9, 8),
    );
    
    var baseRobot = new THREE.Mesh(geoBaseRobot, matRobot);
    baseRobot.position.set(1.5, 0, 0);

    var eje = new THREE.Mesh(geoEje, matRobot);
    eje.rotation.x = Math.PI/2;

    var esparrago = new THREE.Mesh(geoEsparrago, matRobot);
    esparrago.position.set(0, 60, 0);

    var rotula = new THREE.Mesh(geoRotula, matRobot);
    rotula.position.set(0, 120, 0);

    var disco = new THREE.Mesh(geoDisco, matRobot);

    var nervio1 = new THREE.Mesh(geoNervios, matRobot);
    nervio1.position.set(8,40,4);

    var nervio2 = new THREE.Mesh(geoNervios, matRobot);
    nervio2.position.set(8,40,-4);

    var nervio3 = new THREE.Mesh(geoNervios, matRobot);
    nervio3.position.set(-8,40,4);

    var nervio4 = new THREE.Mesh(geoNervios, matRobot);
    nervio4.position.set(-8,40,-4);

    var mano = new THREE.Mesh(geoMano, matRobot);
    mano.rotation.x = Math.PI/2;
    mano.position.set(0,80,0);

    var pinzaI = new THREE.Mesh(geoPinza, matRobot);
    var pinzaD = new THREE.Mesh(geoPinza, matRobot);
    pinzaD.position.set(0, 20, 0);

    brazo = new THREE.Object3D();

    antebrazo = new THREE.Object3D();
    antebrazo.position.set(0, 120, 0);
    
    robot = new THREE.Object3D();
    
    mano.add(pinzaI);
    mano.add(pinzaD);
    
    antebrazo.add(mano);
    antebrazo.add(nervio1);
    antebrazo.add(nervio2);
    antebrazo.add(nervio3);
    antebrazo.add(nervio4);
    antebrazo.add(disco);
    
    brazo.add(antebrazo);
    brazo.add(eje);
    brazo.add(esparrago);
    brazo.add(rotula);
    
    baseRobot.add(brazo);

    robot.add(baseRobot);
    
    scene.add(robot);

    //Añadimos un suelo
    var geoSuelo = new THREE.PlaneGeometry(1000, 1000, 50, 50);
    var suelo = new THREE.Mesh(geoSuelo, matRobot);
    suelo.rotateX(-Math.PI / 2);
    scene.add(suelo);

    //scene.add(new THREE.AxesHelper(2));

    //Suelo
    //Coordinates.drawGround({size:700, offset: -100});

    //Texto
    // var textLoader = new THREE.FontLoader();
    //textLoader.load('fonts/helvetiker_regular.typeface.json', 
      //              function(font){var geoText = new THREE.TextGeometry('A por el bote', 
        //                                                                {
          //                                                                  size: 1, 
            //                                                                height: 0.1, 
              //                                                              curveSegments: 3, 
                //                                                            font: font,
                  //                                                          weight: "bold",
                    //                                                        style: "normal",
                      //                                                      bevelThickness: 0.05,
                        //                                                    bevelSize: 0.04,
                          //                                                  bevelEnable: true
                            //                                            });
                              //      var texto = new THREE.Mesh(geoText, matCubo);
                                //    scene.add(texto);
                                  //  texto.position.set(-2,0,1);
                                    //texto.scale.set(0.5,0.5,0.5);
                  // });
    //Modelo externo
    //var loader = new THREE.ObjectLoader();
    //loader.load('models/captain-america-shield-threejs/captain-america-shield.json',
    //            function(obj) {
    //                obj.position.set(0,1,0);
    //                cubo.add(obj);
    //            });
}

function update()
{
    angulo += 0.01;
    robot.rotation.y = angulo;
}

function render(){
    requestAnimationFrame(render);
    update();
    renderer.render(scene, camera);

}

