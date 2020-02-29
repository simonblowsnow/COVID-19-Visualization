import * as THREE from "three";
import { ThreeLayer } from 'maptalks.three';
import { EffectComposer }  from './libs/EffectComposer';
import RenderPass  from './libs/RenderPass';
import UnrealBloomPass from "./libs/UnrealBloomPass";


function _initBloom () {
    const params = {
        exposure: 1,
        bloomStrength: 4.5,
        bloomThreshold: 0,
        bloomRadius: 0,
        debug: false
    };
    const renderer = this.getThreeRenderer();
    const size = this.getMap().getSize();

    this.composer = new EffectComposer(renderer);
    this.composer.setSize(size.width, size.height);
    

    const scene = this.getScene(), camera = this.getCamera();
    this.renderPass = new RenderPass(scene, camera);

    this.composer.addPass(this.renderPass);

    const bloomPass = this.bloomPass = new UnrealBloomPass(new THREE.Vector2(size.width, size.height));
    bloomPass.renderToScreen = true;
    bloomPass.threshold = params.bloomThreshold;
    bloomPass.strength = params.bloomStrength;
    bloomPass.radius = params.bloomRadius;

    // composer.setSize(size.width, size.height);
    // composer.addPass(renderPass);
    this.composer.addPass(bloomPass);
    this.bloomEnable = true;
}

function setRendererRenderScene () {
    this.getRenderer().renderScene = function () {
        const layer = this.layer;
        layer._callbackBaseObjectAnimation();
        this._syncCamera();

        const renderer = this.context, camera = this.camera, scene = this.scene;
        if (layer.bloomEnable && layer.composer && layer.composer.passes.length > 1) {
            if (renderer.autoClear) {
                renderer.autoClear = false;
            }
            if (layer.bloomPass) {
                camera.layers.set(1);
            }
            if (layer && layer.composer) {
                layer.composer.render(0);
            }
            renderer.clearDepth();
            camera.layers.set(0);
            renderer.render(scene, camera);
        } else {
            if (!renderer.autoClear) {
                renderer.autoClear = true;
            }
            renderer.render(scene, camera);
        }

        this.completeRender();
    }
}

function InitBloom () {
    ThreeLayer.prototype.initBloom = _initBloom;
    ThreeLayer.prototype.setRendererRenderScene = setRendererRenderScene;
}

// InitBloom();

export {InitBloom};