// static/js/index.js

// Initialize the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('scene-container').appendChild(renderer.domElement);

// Load the texture
const textureLoader = new THREE.TextureLoader();
const texture = textureLoader.load('/static/assets/moret.png');

// Add a larger square (cube) with the loaded texture to the scene
const geometry = new THREE.BoxGeometry(3, 3, 3);  // Larger cube
const material = new THREE.MeshBasicMaterial({ map: texture });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

camera.position.z = 5;

// Render loop
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();

// GSAP and ScrollTrigger setup
gsap.registerPlugin(ScrollTrigger);

// Animation for cube rotation based on scroll
gsap.to(cube.rotation, {
    scrollTrigger: {
        trigger: ".content",
        start: "top top",
        end: "bottom bottom",
        scrub: true
    },
    x: Math.PI * 2,
    y: Math.PI * 2,
    duration: 1
});

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
