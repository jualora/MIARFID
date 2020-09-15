/**
* Grafo.js
* Carga un grafo de escena en Threejs y lo visualiza
*
*/

var renderer, scene, camera;

var L = 200;

var robot, base, brazo, anteBrazo, mano, pinzaDerecha, pinzaIzquierda;

var cameraControl;

var effectControl;

var angulo = 0;

init();
loadScene();
setupGUI();
render();

function init() {
    // inicializar Threejs

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0xFFFFFF));
    renderer.autoClear = false;
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();

    setCameras(window.innerWidth / window.innerHeight);

    cameraControl = new THREE.OrbitControls(camera, renderer.domElement);
    cameraControl.target.set(0, 115, 0);
    cameraControl.noKeys = true;

    window.addEventListener('resize', updateAspectRatio);

    window.onkeydown = function (e) {
        var key = e.keyCode ? e.keyCode : e.which;

        if (key == 38) {
            robot.position.x += 2;
        } else if (key == 40) {
            robot.position.x -= 2;
        } else if (key == 37) {
            robot.position.z -= 2;
        } else if (key == 39) {
            robot.position.z += 2;
        }
    };

    // FPS
    stats = new Stats();
    document.getElementById('container').appendChild(stats.domElement);

    window.addEventListener('resize', updateAspectRatio);

}

function setCameras(aspectRatio) {
    // Configurar planta, alzado, perfil y perspectiva
    var camaraOrtografica;
    camaraOrtografica = new THREE.OrthographicCamera(-L, L, L, -L, -1, 1000);
    camaraOrtografica.lookAt(new THREE.Vector3(0, 115, 0));

    planta = camaraOrtografica.clone();
    planta.position.set(0, L, 0);
    planta.up = new THREE.Vector3(0, 0, -1);
    planta.lookAt(new THREE.Vector3(0, 0, 0));

    var camaraPerspectiva = new THREE.PerspectiveCamera(75, aspectRatio, 0.1, 1000);
    camaraPerspectiva.position.set(-140, 220, -140);
    camaraPerspectiva.lookAt(new THREE.Vector3(0, 115, 0));

    camera = camaraPerspectiva.clone();

    scene.add(camera);
    scene.add(planta);
}

function loadScene() {
    // Carga la escena

    var matRobot = new THREE.MeshBasicMaterial({ color: 'red', wireframe: true });

    // Definimos las figuras
    var geoGround = new THREE.PlaneGeometry(1000, 1000, 10, 10);
    var geoBase = new THREE.CylinderGeometry(50, 50, 15, 32);
    var geoEje = new THREE.CylinderGeometry(20, 20, 18, 32);
    var geoEsparrago = new THREE.BoxGeometry(18, 120, 12);
    var geoRotula = new THREE.SphereGeometry(20, 30, 30);
    var geoDisco = new THREE.CylinderGeometry(22, 22, 6, 32);
    var geoNervios = new THREE.BoxGeometry(4, 80, 4);
    var geoMano = new THREE.CylinderGeometry(15, 15, 40, 32);
    var geoPinzas = new THREE.Geometry();
    geoPinzas.vertices.push(
        new THREE.Vector3(0, 0, 0),  // 0
        new THREE.Vector3(0, 20, 0), // 1
        new THREE.Vector3(4, 20, 0), // 2
        new THREE.Vector3(4, 0, 0),  // 3
        new THREE.Vector3(0, 0, 19), // 4
        new THREE.Vector3(0, 20, 19),// 5
        new THREE.Vector3(4, 20, 19),// 6
        new THREE.Vector3(4, 0, 19), // 7
        new THREE.Vector3(2, 5, 38), // 8
        new THREE.Vector3(2, 15, 38),// 9
        new THREE.Vector3(4, 15, 38),// 10
        new THREE.Vector3(4, 5, 38)  // 11
    );
    geoPinzas.faces.push(
        new THREE.Face3(4, 1, 0),
        new THREE.Face3(4, 5, 1),
        new THREE.Face3(1, 3, 0),
        new THREE.Face3(2, 3, 1),
        new THREE.Face3(3, 4, 0),
        new THREE.Face3(7, 4, 3),
        new THREE.Face3(5, 2, 1),
        new THREE.Face3(6, 2, 5),
        new THREE.Face3(7, 3, 2),
        new THREE.Face3(6, 7, 2),
        new THREE.Face3(9, 5, 4),
        new THREE.Face3(4, 8, 9),
        new THREE.Face3(9, 6, 5),
        new THREE.Face3(9, 10, 6),
        new THREE.Face3(11, 4, 7),
        new THREE.Face3(11, 8, 4),
        new THREE.Face3(11, 6, 10),
        new THREE.Face3(11, 7, 6),
        new THREE.Face3(8, 10, 9),
        new THREE.Face3(8, 11, 10)
    );

    // Ponemos la textura a las figuras
    var ground = new THREE.Mesh(geoGround, matRobot);
    base = new THREE.Mesh(geoBase, matRobot);
    var eje = new THREE.Mesh(geoEje, matRobot);
    var esparrago = new THREE.Mesh(geoEsparrago, matRobot);
    var rotula = new THREE.Mesh(geoRotula, matRobot);
    var disco = new THREE.Mesh(geoDisco, matRobot);
    var nervios = new THREE.Mesh(geoNervios, matRobot);
    mano = new THREE.Mesh(geoMano, matRobot);
    pinzaDerecha = new THREE.Mesh(geoPinzas, matRobot);
    pinzaIzquierda = pinzaDerecha.clone();


    // Creamos los links vacíos
    robot = new THREE.Object3D(); // Empty Object de Unity
    brazo = new THREE.Object3D();
    anteBrazo = new THREE.Object3D();

    // Enlazamos los links entre ellos
    robot.add(base);
    base.position.set(0, 7.5, 0);

    // Brazo
    base.add(brazo);

    brazo.add(eje);
    eje.rotation.x = Math.PI / 2;

    brazo.add(esparrago);
    esparrago.position.set(0, 60, 0);

    brazo.add(rotula);
    rotula.position.set(0, 120, 0);

    // Antebrazo
    brazo.add(anteBrazo);
    anteBrazo.position.set(0, 120, 0);

    anteBrazo.add(disco);

    var nervios_cp = nervios.clone();
    anteBrazo.add(nervios_cp);
    nervios_cp.position.set(7, 40, 7);
    nervios_cp = nervios.clone();
    anteBrazo.add(nervios_cp);
    nervios_cp.position.set(7, 40, -7);
    nervios_cp = nervios.clone();
    anteBrazo.add(nervios_cp);
    nervios_cp.position.set(-7, 40, 7);
    nervios_cp = nervios.clone();
    anteBrazo.add(nervios_cp);
    nervios_cp.position.set(-7, 40, -7);

    anteBrazo.add(mano);
    mano.position.set(0, 80, 0);
    mano.rotation.x = -Math.PI / 2;

    mano.add(pinzaDerecha);
    pinzaDerecha.position.set(0, -10, 10);
    pinzaDerecha.rotation.x = -Math.PI / 2;
    pinzaDerecha.rotation.y = -Math.PI / 2;

    mano.add(pinzaIzquierda);
    pinzaIzquierda.position.set(0, 10, -10);
    pinzaIzquierda.rotation.x = Math.PI / 2;
    pinzaIzquierda.rotation.y = -Math.PI / 2;

    // Añadimos el suelo a la escena
    scene.add(ground);
    ground.rotation.x = -Math.PI / 2;

    // Añadimos el robot a la escena
    scene.add(robot);

    // scene.add(new THREE.AxesHelper(50));
}

function setupGUI() {
    // Construye la interfaz de usuario
    effectControl = {
        giroBase: 0,
        giroBrazo: 0,
        giroAntebrazoY: 0,
        giroAntebrazoZ: 0,
        giroPinza: 0,
        separacionPinza: 0
    };

    var gui = new dat.GUI();

    var sub = gui.addFolder("Robot Control");
    sub.add(effectControl, "giroBase", -180, 180, 0.5).name("Giro Base");
    sub.add(effectControl, "giroBrazo", -45, 45, 0.5).name("Giro Brazo");
    sub.add(effectControl, "giroAntebrazoY", -180, 180, 0.5).name("Giro Antebrazo Y");
    sub.add(effectControl, "giroAntebrazoZ", -90, 90, 0.5).name("Giro Antebrazo Z");
    sub.add(effectControl, "giroPinza", -40, 220, 0.5).name("Giro Pinza");
    sub.add(effectControl, "separacionPinza", 0, 15, 0.5).name("Separación Pinza");
}

function updateAspectRatio() {
    // Ajustar la cámara y el viewport a las nuevas dimensiones del canvas
    renderer.setSize(window.innerWidth, window.innerHeight);
    var aspectRatio = window.innerWidth / window.innerHeight;

    camera.aspect = aspectRatio;

    if (aspectRatio < 1) {
        planta.left = -L;
        planta.right = L;
        planta.top = L;
        planta.bottom = -L;
    } else {
        planta.left = -L;
        planta.right = L;
        planta.top = L;
        planta.bottom = -L;
    }
    planta.updateProjectionMatrix();
    camera.updateProjectionMatrix();
}

function update() {
    base.rotation.y = effectControl.giroBase * (Math.PI / 180);
    brazo.rotation.z = effectControl.giroBrazo * (Math.PI / 180);
    anteBrazo.rotation.y = effectControl.giroAntebrazoY * (Math.PI / 180);
    anteBrazo.rotation.z = effectControl.giroAntebrazoZ * (Math.PI / 180);
    mano.rotation.y = effectControl.giroPinza * (Math.PI / 180);
    pinzaIzquierda.position.y = 4 + effectControl.separacionPinza;
    pinzaDerecha.position.y = -4 - effectControl.separacionPinza;

    stats.update();
}

function render() {
    requestAnimationFrame(render);
    update();
    renderer.clear();

    renderer.setViewport(0, 0, window.innerWidth, window.innerHeight);
    renderer.render(scene, camera);

    renderer.setViewport(0, 0, Math.min(window.innerWidth, window.innerHeight) / 4, Math.min(window.innerWidth, window.innerHeight) / 4);
    renderer.render(scene, planta);
}
