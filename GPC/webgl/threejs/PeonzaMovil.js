/**
 * PeonzaMovil.js
 * Construir una peonza que gire en un plano con rebotes
 *
 */

var renderer, scene, camera;

var cameraControls;

var effectControl;

var stats;

var angulo = 0;
var peonza;
var antes = Date.now();

init();
loadScene();
setupGUI();
startAnimation();
render();

function init() {
    //Inicializar Threejs
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0x0000AA));
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 100);

    camera.position.set(0.5, 2, 5);
    camera.lookAt(new THREE.Vector3(0,0,0));

    cameraControls = new THREE.OrbitControls(camera, renderer.domElement);
    cameraControls.target.set(0,0,0);

    //FPS
    stats = new Stats();
    document.getElementById('container').appendChild(stats.domElement);

    window.addEventListener('resize', updateAspectRatio);
}

function loadScene() {
    //Cargar la escena

    //Materiales
    var material = new THREE.MeshBasicMaterial({color:'yellow', wireframe:true});

    //Objetos
    var cuerpo = new THREE.Mesh(new THREE.CylinderGeometry(1,0.2,2,10,2), material);
    var punta = new THREE.Mesh(new THREE.CylinderGeometry(0.1,0,0.5,10,1), material);
    var mango = new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.1,0.5,10,1), material);

    peonza = new THREE.Object3D();
    cuerpo.position.y = 1.5;
    punta.position.y = 0.25;
    mango.position.y = 2.75;

    peonza.add(cuerpo);
    peonza.add(punta);
    peonza.add(mango);

    scene.add(peonza);
}

function setupGUI(){
    //Construye la interfaz de usuario
    effectControl = {mensaje: 'Interfaz', velang: 1.0, reiniciar: function(){angulo = 0;}, color: 'rgb(255,255,0)'};
    
    var gui = new dat.GUI();

    var sub = gui.addFolder("Controles Peonza");
    sub.add(effectControl, "mensaje").name("Peonza");
    sub.add(effectControl, "velang", 0.0, 5.0, 0.5).name("Vueltas/sg");
    sub.add(effectControl, "reiniciar").name("Reiniciar");
    var sensorColor = sub.addColor(effectControl, "color").name("Color");
    sensorColor.onChange(function(color){peonza.traverse(function(hijo){if(hijo instanceof THREE.Mesh){hijo.material.color = new THREE.Color(color);}})});
}

function updateAspectRatio(){
    //Conservar isotropía
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
}

function startAnimation(){
    //Interpola movimientos de los objetos de la escena
    var mvtoIzq = new TWEEN.Tween(peonza.position).to({x:[-1.5, -2.5], y:[0,0], z:[0, 2.5]}, 5000);
    var mvtoFrt = new TWEEN.Tween(peonza.position).to({x:[0, 2.5], y:[0,0], z:[1.5,2.5]}, 5000);
    var mvtoDrc = new TWEEN.Tween(peonza.position).to({x:[1.5, 2.5], y:[0,0], z:[0, -2.5]}, 5000);
    var mvtoTrs = new TWEEN.Tween(peonza.position).to({x:[0, -2.5], y:[0,0], z:[-1.5, -2.5]}, 5000);

    mvtoIzq.easing(TWEEN.Easing.Bounce.Out);
    mvtoIzq.interpolation(TWEEN.Interpolation.Bezier);

    mvtoFrt.easing(TWEEN.Easing.Bounce.Out);
    mvtoFrt.interpolation(TWEEN.Interpolation.Bezier);

    mvtoDrc.easing(TWEEN.Easing.Bounce.Out);
    mvtoDrc.interpolation(TWEEN.Interpolation.Bezier);

    mvtoTrs.easing(TWEEN.Easing.Bounce.Out);
    mvtoTrs.interpolation(TWEEN.Interpolation.Bezier);

    mvtoIzq.chain(mvtoFrt);
    mvtoFrt.chain(mvtoDrc);
    mvtoDrc.chain(mvtoTrs);
    mvtoTrs.chain(mvtoIzq);

    mvtoIzq.start();
}

function update()
{
    var ahora = Date.now();

    angulo += effectControl.velang * 2*Math.PI * (ahora-antes)/1000; //radianes
    peonza.rotation.y = angulo;

    antes = ahora;

    stats.update();

    TWEEN.update();
}

function render(){
    requestAnimationFrame(render);
    update();
    renderer.render(scene, camera);

}

