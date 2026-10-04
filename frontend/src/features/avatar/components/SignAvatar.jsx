import React, { Suspense, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import {
  Environment,
  OrbitControls,
  useGLTF,
} from "@react-three/drei";

const MODEL_URL = import.meta.env.VITE_AVATAR_MODEL_URL || "";

function ProceduralAvatar({ gesture }) {
  const root = useRef(null);
  const leftArm = useRef(null);
  const rightArm = useRef(null);

  useFrame(({ clock }) => {
    const time = clock.getElapsedTime();

    if (root.current) {
      root.current.rotation.y = Math.sin(time * 0.45) * 0.035;
    }

    if (gesture === "wave" && rightArm.current) {
      rightArm.current.rotation.z =
        -0.8 + Math.sin(time * 6) * 0.28;
    }

    if (gesture === "sign") {
      if (leftArm.current) {
        leftArm.current.rotation.z =
          -0.55 + Math.sin(time * 4) * 0.12;
      }

      if (rightArm.current) {
        rightArm.current.rotation.z =
          0.55 + Math.cos(time * 4) * 0.12;
      }
    }

    if (gesture === "idle") {
      if (leftArm.current) {
        leftArm.current.rotation.z = -0.15;
      }

      if (rightArm.current) {
        rightArm.current.rotation.z = 0.15;
      }
    }
  });

  return (
    <group ref={root} position={[0, -1.6, 0]}>
      {/* Head */}
      <mesh position={[0, 2.25, 0]}>
        <sphereGeometry args={[0.42, 32, 32]} />
        <meshStandardMaterial roughness={0.7} />
      </mesh>

      {/* Body */}
      <mesh position={[0, 1.25, 0]}>
        <capsuleGeometry args={[0.5, 1.05, 8, 16]} />
        <meshStandardMaterial roughness={0.8} />
      </mesh>

      {/* Left Arm */}
      <group ref={leftArm} position={[-0.58, 1.55, 0]}>
        <mesh position={[0, -0.48, 0]}>
          <capsuleGeometry args={[0.13, 0.8, 6, 12]} />
          <meshStandardMaterial roughness={0.78} />
        </mesh>
      </group>

      {/* Right Arm */}
      <group ref={rightArm} position={[0.58, 1.55, 0]}>
        <mesh position={[0, -0.48, 0]}>
          <capsuleGeometry args={[0.13, 0.8, 6, 12]} />
          <meshStandardMaterial roughness={0.78} />
        </mesh>
      </group>

      {/* Left Leg */}
      <mesh position={[-0.22, 0.15, 0]}>
        <capsuleGeometry args={[0.15, 0.9, 6, 12]} />
        <meshStandardMaterial roughness={0.8} />
      </mesh>

      {/* Right Leg */}
      <mesh position={[0.22, 0.15, 0]}>
        <capsuleGeometry args={[0.15, 0.9, 6, 12]} />
        <meshStandardMaterial roughness={0.8} />
      </mesh>
    </group>
  );
}

function LoadedAvatar() {
  const { scene } = useGLTF(MODEL_URL);

  return (
    <primitive
      object={scene}
      position={[0, -1.65, 0]}
      scale={2.25}
    />
  );
}

function AvatarScene({ gesture }) {
  return (
    <>
      <ambientLight intensity={1.5} />

      <directionalLight
        position={[4, 6, 5]}
        intensity={2.4}
      />

      <directionalLight
        position={[-4, 2, -3]}
        intensity={1.1}
      />

      {MODEL_URL ? (
        <Suspense
          fallback={<ProceduralAvatar gesture={gesture} />}
        >
          <LoadedAvatar />
        </Suspense>
      ) : (
        <ProceduralAvatar gesture={gesture} />
      )}

      <Environment preset="studio" />

      <OrbitControls
        enablePan={false}
        minDistance={2.4}
        maxDistance={7}
        target={[0, 1.1, 0]}
      />
    </>
  );
}

export default function SignAvatar({ gesture = "idle" }) {
  return (
    <Canvas
      camera={{
        position: [0, 1.3, 4.4],
        fov: 40,
      }}
      dpr={[1, 2]}
      gl={{
        antialias: true,
      }}
    >
      <color attach="background" args={["#0b1018"]} />
      <AvatarScene gesture={gesture} />
    </Canvas>
  );
}
