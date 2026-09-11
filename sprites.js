// --- 12x18 Detailed Retro Pixel Sprite Definitions ---
const PALETTES = {
  skin: ["#d59b7d", "#e5b887", "#f3cfab"],
  steel: ["#2d3748", "#4a5568", "#a0aec0", "#edf2f7"],
  gold: ["#744210", "#b7791f", "#ecc94b"],
  leather: ["#3b2219", "#5c3a21", "#8b5a2b"],
  wood: ["#271912", "#4a2d18", "#784b28"],
  player_fabric: ["#1a365d", "#2b4c7e", "#4299e1", "#bee3f8"],
  enemy_fabric:  ["#4c1d24", "#742a2a", "#e53e3e", "#fed7d7"],
  bloom_graft:   ["#1c3821", "#276749", "#48bb78", "#9ae6b4"],
  fire:          ["#7b1113", "#dd6b20", "#ecc94b", "#ffffff"]
};

// 12 columns by 18 rows pixel maps
const SPRITE_MAPS = {
  Vanguard: [
    "....GGGG....",
    "...GMMMMG...",
    "...MMMMMM...",
    "...MSDSDM...",
    "...MSSSSM...",
    "..FFAAAAFF..",
    ".SFAAAASAS..",
    ".SFAAAAAAS..",
    ".SFAAAAAAS..",
    ".SFAAAAAFF..",
    "..FAAAAAM...",
    "..LL..LLM...",
    "..LL..LLM...",
    "..LL..LL....",
    "..MM..MM....",
    "..MM..MM....",
    "............",
    "..xxxxxxxxx."
  ],
  Halberdier: [
    "....MMMM....",
    "...MMMMMM...",
    "...MSSSSM...",
    "...SDSDSD...",
    "....SSSS....",
    "..FFAAAAFF.W",
    ".FFAAAAAFF.W",
    ".FFAAAAAFF.W",
    "..FAAAAAM..W",
    "..FAAAAA...W",
    "..LL..LL...W",
    "..LL..LL..MW",
    "..LL..LL.MMM",
    "..MM..MM..M.",
    "..MM..MM....",
    "..MM..MM....",
    "............",
    "..xxxxxxxxx."
  ],
  Archer: [
    "....LLLL....",
    "...LLLLLL...",
    "...LSDSDL...",
    "...LSSSSL...",
    "....SSSS....",
    "..FFAAAAFF.B",
    ".LFAAAAAFF.B",
    ".LFAAAAAFB.B",
    ".LFAAAAAM..B",
    "..FAAAAAM..B",
    "..LL..LL...B",
    "..LL..LL..B.",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "............",
    "..xxxxxxxxx."
  ],
  Flyer: [
    "....MMMM....",
    "...MMMMMM...",
    "...MSDSDM...",
    "W..MSSSSM..W",
    "WW.FFAAAAFFWW",
    "WWWFFAAAAAFWW",
    "WWWFAAAAAAMWW",
    ".WWFAAAAAAMWS",
    "..WFAAAAAM..S",
    "..WLL..LL...S",
    "...LL..LL...S",
    "...LL..LL...S",
    "...LL..LL...S",
    "...MM..MM....",
    "...MM..MM....",
    "...MM..MM....",
    "............",
    "..xxxxxxxxx."
  ],
  Pyromancer: [
    "....FFFF....",
    "...FFFFFF...",
    "...FSDDSF...",
    "...FSSSSFF..",
    "....SSSS....",
    "..FFAAAAFF..",
    ".FFAAAAAFFP.",
    ".FFAAAAAFPFP",
    "..FAAAAAFFP.",
    "..FAAAAAM...",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "..FF..FF....",
    "..FF..FF....",
    "..FF..FF....",
    "............",
    "..xxxxxxxxx."
  ],
  Warden: [
    "....LLLL....",
    "...LSSSSM...",
    "...MSDSDM...",
    "...MSSSSM...",
    "....SSSS..G.",
    "..MMAAAAMMGG",
    ".MMAAAAAAMGG",
    ".MMAAAAAAMGG",
    "..MAAAAAM.GG",
    "..MAAAAAM.GG",
    "..LL..LL..GG",
    "..LL..LL..GG",
    "..LL..LL..GG",
    "..MM..MM....",
    "..MM..MM....",
    "..MM..MM....",
    "............",
    "..xxxxxxxxx."
  ],
  Apothecary: [
    "....LLLL....",
    "...LLLLLL...",
    "...LSDSDL...",
    "...LSSSSL...",
    "....SSSS....",
    "..FFAAAAFF..",
    ".FFAAAAAFFV.",
    ".FFAAAAAFFVV",
    "..LAAAAAL.V.",
    "..LAAAAAL...",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "............",
    "..xxxxxxxxx."
  ],
  Duelist: [
    "....FFFF....",
    "...FFFFFF...",
    "...FSDDSF...",
    "...FSSSSF...",
    "....SSSS....",
    "..FFAAAAFF..",
    ".SFAAAAAFFC.",
    ".SFAAAAAFCC.",
    "..FAAAAAM.C.",
    "..FAAAAAM.C.",
    "..LL..LL..C.",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "..LL..LL....",
    "............",
    "..xxxxxxxxx."
  ],
  Grafted: [
    "....BBBB....",
    "...BBBBBB...",
    "...BSDSSB...",
    "...BSSSSB...",
    "....SSSS....",
    "..BBAAAABB..",
    ".BBAAAAAABB.",
    ".BBAAAAAABBB",
    "..BAAAAAB.B.",
    "..BAAAAAB...",
    "..BB..BB....",
    "..BB..BB....",
    "..BB..BB....",
    "..BB..BB....",
    "..BB..BB....",
    "..BB..BB....",
    "............",
    "..xxxxxxxxx."
  ]
};

function drawDetailedUnitSprite(ctx, u, screenX, screenY, tileSize, animationPulse, DIRS) {
  const map = SPRITE_MAPS[u.role] || SPRITE_MAPS["Vanguard"];
  const isPlayer = (u.faction === "PLAYER");
  const isFlashing = (u.flashRedTimer > 0);

  const pFabric = isFlashing ? "#ff3333" : (isPlayer ? PALETTES.player_fabric[1] : PALETTES.enemy_fabric[1]);
  const pArmor  = isFlashing ? "#ffffff" : (isPlayer ? PALETTES.player_fabric[2] : PALETTES.enemy_fabric[2]);

  const pSize = 2;
  const bob = u.isFlying ? Math.sin(animationPulse * 2) * 3 : 0;
  const startX = Math.round(screenX + (tileSize - (12 * pSize)) / 2 + u.offsetX);
  const startY = Math.round(screenY + (tileSize - (18 * pSize)) / 2 + u.offsetY + bob);

  // Large Wings for Flying Units
  if (u.isFlying) {
    ctx.save();
    ctx.fillStyle = isFlashing ? "#ff6666" : "#edf2f7";
    ctx.strokeStyle = isFlashing ? "#ffffff" : "#a0aec0";
    ctx.lineWidth = 1.2;

    const wingCenterX = screenX + tileSize / 2 + u.offsetX;
    const wingCenterY = screenY + tileSize / 2 - 4 + u.offsetY + bob;

    // Left Wing
    ctx.beginPath();
    ctx.ellipse(wingCenterX - 18, wingCenterY - 6, 14, 6, -0.35, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.beginPath();
    ctx.ellipse(wingCenterX - 13, wingCenterY, 10, 4, -0.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Right Wing
    ctx.beginPath();
    ctx.ellipse(wingCenterX + 18, wingCenterY - 6, 14, 6, 0.35, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.beginPath();
    ctx.ellipse(wingCenterX + 13, wingCenterY, 10, 4, 0.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.restore();
  }

  for (let r = 0; r < 18; r++) {
    for (let c = 0; c < 12; c++) {
      let char = map[r][c];
      if (char === '.') continue;

      let col = null;
      switch (char) {
        case 'x': col = "rgba(0,0,0,0.35)"; break;
        case 'S': col = PALETTES.skin[1]; break;
        case 'D': col = PALETTES.skin[0]; break;
        case 'M': col = PALETTES.steel[2]; break;
        case 'G': col = PALETTES.gold[1]; break;
        case 'L': col = PALETTES.leather[1]; break;
        case 'W': col = u.isFlying ? "#ffffff" : PALETTES.wood[1]; break;
        case 'B': col = (u.role === "Grafted") ? PALETTES.bloom_graft[1] : PALETTES.wood[2]; break;
        case 'F': col = pFabric; break;
        case 'A': col = pArmor; break;
        case 'P': col = PALETTES.fire[Math.floor(Math.random()*4)]; break;
        case 'V': col = "#56d364"; break;
        case 'C': col = PALETTES.steel[3]; break;
      }

      if (col) {
        ctx.fillStyle = col;
        ctx.fillRect(startX + c * pSize, startY + r * pSize, pSize, pSize);
      }
    }
  }

  if (u.staggered) {
    ctx.fillStyle = "#f85149";
    ctx.font = "bold 9px monospace";
    ctx.fillText("STUN", screenX + tileSize / 2 - 12 + u.offsetX, screenY + 10 + u.offsetY);
  }

  // Directional facing indicator chevron
  ctx.fillStyle = isPlayer ? "#58a6ff" : "#f85149";
  let off = 16;
  let cx = screenX + tileSize / 2 + u.offsetX;
  let cy = screenY + tileSize / 2 + u.offsetY;
  ctx.beginPath();
  if (u.facing === DIRS.NORTH) { ctx.moveTo(cx, cy - off); ctx.lineTo(cx - 3, cy - off + 4); ctx.lineTo(cx + 3, cy - off + 4); }
  if (u.facing === DIRS.SOUTH) { ctx.moveTo(cx, cy + off); ctx.lineTo(cx - 3, cy + off - 4); ctx.lineTo(cx + 3, cy + off - 4); }
  if (u.facing === DIRS.EAST)  { ctx.moveTo(cx + off, cy); ctx.lineTo(cx + off - 4, cy - 3); ctx.lineTo(cx + off - 4, cy + 3); }
  if (u.facing === DIRS.WEST)  { ctx.moveTo(cx - off, cy); ctx.lineTo(cx - off + 4, cy - 3); ctx.lineTo(cx - off + 4, cy + 3); }
  ctx.fill();

  // Mini Health Bar
  let barW = tileSize - 10;
  ctx.fillStyle = "#21262d";
  ctx.fillRect(screenX + 5 + u.offsetX, screenY + tileSize - 6 + u.offsetY, barW, 2.5);
  ctx.fillStyle = isPlayer ? "#58a6ff" : "#f85149";
  ctx.fillRect(screenX + 5 + u.offsetX, screenY + tileSize - 6 + u.offsetY, barW * Math.max(0, u.hp / u.maxHp), 2.5);
}