/**
 * Redskill 注入器(openclaw before_prompt_build hook)。
 *
 * 思路:
 *  1. 触发判定走可配置短语表 + 默认中文/英文混合词典,避免单条 regex 难以维护。
 *  2. 注入文本由 PolicyBuilder 拼接,verbosity 三档(compact/normal/detailed)。
 *  3. registries 数组驱动 fallback 顺序,不写死「primary/fallback」二元。
 *  4. 头部带 [redskill@<version>] 版本戳,便于事后对照是哪一版策略生效。
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

const PLUGIN_VERSION = "0.1.0";

type Registry = { cli: string; label: string; scope?: string };

type RedskillConfig = {
  team?: string;
  registries?: Registry[];
  triggerPhrases?: string[];
  verbosity?: "compact" | "normal" | "detailed";
  stampVersion?: boolean;
};

const DEFAULT_TRIGGERS = [
  "skill", "skills",
  "技能", "找技能", "小红书技能", "笔记技能", "redskill",
  "插件", "能力扩展",
];

const DEFAULT_REGISTRIES: Registry[] = [
  { cli: "redskill", label: "小红书内部", scope: "internal" },
  { cli: "clawhub",  label: "公网兜底",    scope: "public" },
];

function trim(value: unknown): string | null {
  if (typeof value !== "string") return null;
  const out = value.trim();
  return out ? out : null;
}

function lc(value: string): string {
  return value.toLowerCase();
}

class TriggerMatcher {
  private readonly needles: string[];

  constructor(phrases: string[]) {
    const cleaned = phrases.map(trim).filter((p): p is string => !!p);
    const source = cleaned.length > 0 ? cleaned : DEFAULT_TRIGGERS;
    this.needles = source.map(lc);
  }

  hits(prompt: unknown): boolean {
    if (typeof prompt !== "string" || !prompt) return false;
    const haystack = lc(prompt);
    return this.needles.some((n) => haystack.includes(n));
  }
}

function normalizeRegistries(raw: unknown): Registry[] {
  if (!Array.isArray(raw)) return DEFAULT_REGISTRIES;
  const out: Registry[] = [];
  for (const item of raw) {
    if (!item || typeof item !== "object") continue;
    const cli = trim((item as any).cli);
    const label = trim((item as any).label);
    if (!cli || !label) continue;
    const scope = trim((item as any).scope) ?? undefined;
    out.push({ cli, label, ...(scope ? { scope } : {}) });
  }
  return out.length > 0 ? out : DEFAULT_REGISTRIES;
}

class PolicyBuilder {
  constructor(
    private readonly registries: Registry[],
    private readonly verbosity: "compact" | "normal" | "detailed",
    private readonly team?: string,
  ) {}

  build(): string {
    const head = this.buildHead();
    if (this.verbosity === "compact") {
      return head + "\n" + this.compactLine();
    }
    const sections = [head, this.priorityBlock()];
    if (this.verbosity === "detailed") {
      sections.push(this.exampleBlock());
    }
    sections.push(this.constraintBlock());
    return sections.join("\n\n");
  }

  private buildHead(): string {
    const teamLine = this.team ? `业务团队: ${this.team}` : "业务团队: 未指定";
    return `## Redskill 检索策略\n${teamLine}`;
  }

  private compactLine(): string {
    const order = this.registries.map((r) => `${r.cli}(${r.label})`).join(" → ");
    return `优先级: ${order}。安装前必报来源/版本/风险摘要。`;
  }

  private priorityBlock(): string {
    const lines = ["**Registry 优先级(从前往后,失败立即降级)**:"];
    this.registries.forEach((r, i) => {
      const tag = r.scope ? ` _(${r.scope})_` : "";
      lines.push(`${i + 1}. \`${r.cli}\` — ${r.label}${tag}`);
    });
    return lines.join("\n");
  }

  private constraintBlock(): string {
    const primary = this.registries[0]?.cli ?? "redskill";
    return [
      "**约束**",
      `- 搜索请求:先执行 \`${primary} search <关键词>\`,把命令原始输出贴回给用户。`,
      "- 安装前必须告知:来源 registry、版本号、风险信号(签名缺失 / 三方依赖等)。",
      "- 不得宣称排他性 —— 内部与公网 registry 都允许出现。",
      "- 进度更新直接回复,不要为「正在搜索…」单独调 message 工具。",
    ].join("\n");
  }

  private exampleBlock(): string {
    const primary = this.registries[0]?.cli ?? "redskill";
    const fallback = this.registries[1]?.cli;
    const fallbackHint = fallback
      ? `\`${primary} search\` 无结果 → 改 \`${fallback} search\` 并显式说明已降级。`
      : `\`${primary} search\` 无结果 → 直接告知用户找不到。`;
    return ["**示例**", `- ${fallbackHint}`].join("\n");
  }
}

type PolicySettings = {
  team?: string;
  registries: Registry[];
  verbosity: "compact" | "normal" | "detailed";
  stampVersion: boolean;
};

function readPolicy(raw?: Record<string, unknown>): PolicySettings {
  const cfg = (raw ?? {}) as RedskillConfig;
  const verbosity = cfg.verbosity && ["compact", "normal", "detailed"].includes(cfg.verbosity)
    ? cfg.verbosity
    : "normal";
  return {
    team: trim(cfg.team) ?? undefined,
    registries: normalizeRegistries(cfg.registries),
    verbosity,
    stampVersion: cfg.stampVersion !== false,
  };
}

function readMatcher(raw?: Record<string, unknown>): TriggerMatcher {
  const cfg = (raw ?? {}) as RedskillConfig;
  return new TriggerMatcher(cfg.triggerPhrases ?? []);
}

export default function register(api: OpenClawPluginApi) {
  const raw = api.pluginConfig as Record<string, unknown> | undefined;
  const policy = readPolicy(raw);
  const matcher = readMatcher(raw);

  api.on(
    "before_prompt_build",
    async (event) => {
      if (!matcher.hits(event?.prompt)) return;
      const text = new PolicyBuilder(policy.registries, policy.verbosity, policy.team).build();
      const stamp = policy.stampVersion ? `<!-- redskill@${PLUGIN_VERSION} -->\n` : "";
      return { prependContext: stamp + text };
    },
    { priority: 80 },
  );
}
