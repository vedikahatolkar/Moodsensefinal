import React, { useRef, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import * as THREE from "three";

function Model({ url, mood }) {
  const group = useRef();
  const { scene, animations } = useGLTF(url);
  const mixer = useRef(null);
  const actions = useRef({});

  useEffect(() => {
    if (!scene) return;
    mixer.current = new THREE.AnimationMixer(scene);
    animations.forEach((clip) => {
      const name = clip.name.toLowerCase();
      actions.current[name] = mixer.current.clipAction(clip);
    });
    // play first or idle
    const idle = actions.current["idle"] || Object.values(actions.current)[0];
    if (idle) {
      idle.reset().play();
    }
  }, [scene, animations]);

  useFrame((_, delta) => {
    if (mixer.current) mixer.current.update(delta);
  });

  useEffect(() => {
    if (!actions.current) return;
    const map = {
      happy: "smile",
      sad: "sad",
      angry: "angry",
      neutral: "idle",
      wave: "wave",
    };
    const clipName = map[mood] || "idle";

    Object.values(actions.current).forEach((a) => a.fadeOut(0.2));
    const action = actions.current[clipName];
    if (action) {
      action.reset().fadeIn(0.2).play();
    }
  }, [mood]);

  return <primitive ref={group} object={scene} scale={2} position={[0, -1.5, 0]} />;
}

export default function ChatAvatar({ modelUrl = "/models/woody.glb", mood = "neutral" }) {
  return (
    <div style={{ width: "100%", height: 400 }}>
      <Canvas camera={{ position: [0, 1.5, 5] }}>
        <ambientLight intensity={0.9} />
        <directionalLight intensity={1} position={[10, 10, 5]} />
        <React.Suspense fallback={null}>
          <Model url={modelUrl} mood={mood} />
        </React.Suspense>
        <OrbitControls enableZoom={true} />
      </Canvas>
    </div>
  );
}
