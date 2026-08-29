import {
  AbsoluteFill,
  Composition,
  Img,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  CalculateMetadataFunction,
} from "remotion";

// ── Tipos ──────────────────────────────────────────────────────────────────────
export type Scene = {
  index: number;
  titulo?: string;
  descripcion?: string;
  texto_pantalla?: string;
  imagen_path?: string;
  duracion_seg: number;
};

export type Props = {
  project_name?: string;
  tipo_contenido?: "Imagen" | "Video";
  scenes?: Scene[];
  estilo?: { id: string; nombre: string };
  dimensiones?: string;
  fps?: number;
};

// ── Paleta ─────────────────────────────────────────────────────────────────────
const PALETA = [
  "#0f172a", "#0c1a2e", "#1a0a2e", "#0a1a1a", "#1a0a0a",
  "#0a1a0a", "#1a1a0a", "#1a0a1a", "#0a0a1a", "#0a1a0a",
];

const ACCENT = "#8B5CF6";

// ── Slide individual ───────────────────────────────────────────────────────────
const Slide: React.FC<{
  scene: Scene;
  startFrame: number;
  durationFrames: number;
  accent: string;
  bgColor: string;
}> = ({ scene, startFrame, durationFrames, accent, bgColor }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  const opacity = interpolate(localFrame, [0, 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(localFrame, [5, 25], [40, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const fadeOut = interpolate(
    localFrame,
    [durationFrames - 10, durationFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const finalOpacity = opacity * fadeOut;
  const hasImage = Boolean(scene.imagen_path);
  const texto = scene.texto_pantalla || scene.titulo || scene.descripcion || "";

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bgColor,
        opacity: finalOpacity,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {hasImage && (
        <AbsoluteFill>
          <Img
            src={scene.imagen_path!}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
          <AbsoluteFill
            style={{
              background:
                "linear-gradient(to top, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.25) 60%, rgba(0,0,0,0.05) 100%)",
            }}
          />
        </AbsoluteFill>
      )}

      <div
        style={{
          position: "absolute",
          top: 40,
          left: 40,
          background: accent,
          color: "white",
          fontFamily: "sans-serif",
          fontWeight: 700,
          fontSize: 28,
          padding: "8px 18px",
          borderRadius: 8,
          letterSpacing: 2,
        }}
      >
        {String(scene.index).padStart(2, "0")}
      </div>

      <div
        style={{
          width: "100%",
          padding: "0 56px 80px 56px",
          transform: `translateY(${translateY}px)`,
          zIndex: 10,
        }}
      >
        {scene.titulo && (
          <p
            style={{
              fontFamily: "sans-serif",
              fontWeight: 800,
              fontSize: 56,
              color: "#FFFFFF",
              lineHeight: 1.15,
              marginBottom: 16,
              textShadow: "0 2px 12px rgba(0,0,0,0.8)",
            }}
          >
            {scene.titulo}
          </p>
        )}
        {texto && texto !== scene.titulo && (
          <p
            style={{
              fontFamily: "sans-serif",
              fontWeight: 400,
              fontSize: 32,
              color: "rgba(255,255,255,0.88)",
              lineHeight: 1.45,
              textShadow: "0 1px 8px rgba(0,0,0,0.7)",
            }}
          >
            {texto}
          </p>
        )}
        <div
          style={{
            marginTop: 32,
            height: 4,
            width: "100%",
            background: "rgba(255,255,255,0.15)",
            borderRadius: 2,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              height: "100%",
              width: `${(localFrame / durationFrames) * 100}%`,
              background: accent,
              borderRadius: 2,
            }}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── Componente principal ───────────────────────────────────────────────────────
export const BriefVideoComponent: React.FC<Props> = ({
  project_name = "Proyecto",
  scenes = [],
  estilo = { id: "default", nombre: "Editorial" },
  fps = 30,
}) => {
  const { durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();

  const defaultScene: Scene = {
    index: 1,
    titulo: project_name,
    descripcion: "Conexion Python - Remotion activa!",
    duracion_seg: 5,
  };
  const activeScenes = scenes.length > 0 ? scenes : [defaultScene];

  let accFrames = 0;
  let activeSlide: {
    scene: Scene;
    startFrame: number;
    durationFrames: number;
  } | null = null;

  for (let i = 0; i < activeScenes.length; i++) {
    const s = activeScenes[i];
    const dur = Math.max(1, Math.round(s.duracion_seg * fps));
    if (frame >= accFrames && frame < accFrames + dur) {
      activeSlide = { scene: s, startFrame: accFrames, durationFrames: dur };
      break;
    }
    accFrames += dur;
  }

  if (!activeSlide) {
    const last = activeScenes[activeScenes.length - 1];
    const lastDur = Math.max(1, Math.round(last.duracion_seg * fps));
    activeSlide = {
      scene: last,
      startFrame: accFrames - lastDur,
      durationFrames: lastDur,
    };
  }

  const bgIndex = (activeSlide.scene.index - 1) % PALETA.length;

  return (
    <AbsoluteFill style={{ backgroundColor: PALETA[bgIndex] }}>
      <Slide
        scene={activeSlide.scene}
        startFrame={activeSlide.startFrame}
        durationFrames={activeSlide.durationFrames}
        accent={ACCENT}
        bgColor={PALETA[bgIndex]}
      />
    </AbsoluteFill>
  );
};

// ── CalculateMetadata para durationInFrames dinamico ──────────────────────────
const calculateMetadata: CalculateMetadataFunction<Props> = ({ props }) => {
  const fps = props.fps ?? 30;
  const scenes = props.scenes ?? [];

  let width = 1080;
  let height = 1350;
  if (props.dimensiones) {
    if (props.dimensiones.includes("1080x1920")) { height = 1920; }
    else if (props.dimensiones.includes("1080x1080")) { height = 1080; }
    else if (props.dimensiones.includes("1920x1080")) { width = 1920; height = 1080; }
  }

  const totalFrames =
    scenes.length > 0
      ? scenes.reduce(
          (acc, s) => acc + Math.max(1, Math.round((s.duracion_seg ?? 5) * fps)),
          0
        )
      : fps * 5;

  return { durationInFrames: totalFrames, fps, width, height };
};

// ── Registro ───────────────────────────────────────────────────────────────────
export const MyComposition: React.FC = () => {
  return (
    <Composition
      id="MiVideo"
      component={BriefVideoComponent}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1350}
      calculateMetadata={calculateMetadata}
      defaultProps={{
        project_name: "Demo",
        tipo_contenido: "Video",
        scenes: [
          { index: 1, titulo: "Escena Demo", descripcion: "Texto demo", duracion_seg: 5 },
        ],
        estilo: { id: "default", nombre: "Editorial" },
        dimensiones: "4:5 (1080x1350)",
        fps: 30,
      }}
    />
  );
};
