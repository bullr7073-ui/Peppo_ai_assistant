export default function Orb() {
  return (
    <div className="relative w-[280px] h-[280px] rounded-full overflow-hidden border-2 border-white shadow-[0_18px_44px_-8px_rgba(255,209,56,0.35)]">

      {/* Outer ring */}
      <div className="absolute inset-[2px] rounded-full border-2 border-white/55" />

      {/* Main warm gradient */}
      <div
        className="
          absolute inset-0
          rounded-full
          bg-[radial-gradient(circle_at_50%_45%,#FFF9F0_0%,#FFD83D_35%,#FFA04D_70%,#FF8C5A_100%)]
        "
      />

      {/* White upper glow */}
      <div
        className="
          absolute
          w-[220px]
          h-[110px]
          -top-[30px]
          left-[30px]
          rounded-full
          bg-white/80
          blur-[3px]
        "
      />

      {/* Yellow glow */}
      <div
        className="
          absolute
          w-[260px]
          h-[140px]
          -left-[20px]
          top-[120px]
          rounded-full
          bg-[#FFD83D]/60
          blur-[3px]
        "
      />

      {/* Orange glow */}
      <div
        className="
          absolute
          w-[300px]
          h-[160px]
          -left-[10px]
          top-[150px]
          rounded-full
          bg-[#FFE36E]/50
          blur-[4px]
        "
      />

      {/* Soft center glow */}
      <div
        className="
          absolute
          inset-0
          rounded-full
          bg-[radial-gradient(circle_at_50%_50%,rgba(255,249,240,0.25),transparent_65%)]
        "
      />

      {/* Left eye */}
      <div
        className="
          absolute
          w-[36px]
          h-[50px]
          left-[60px]
          top-[100px]
          rounded-full
          bg-white
          shadow-[0_2px_8px_rgba(0,0,0,0.08)]
        "
      />

      {/* Right eye */}
      <div
        className="
          absolute
          w-[36px]
          h-[50px]
          right-[60px]
          top-[100px]
          rounded-full
          bg-white
          shadow-[0_2px_8px_rgba(0,0,0,0.08)]
        "
      />

    </div>
  );
}