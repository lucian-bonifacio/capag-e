export function decimalToMinorUnits(value: string): bigint {
  const normalized = value.trim().replace(",", ".");
  const negative = normalized.startsWith("-");
  const unsigned = normalized.replace(/^-/, "");
  const [integerPart = "0", decimalPart = ""] = unsigned.split(".");
  const cents = `${integerPart.replace(/\D/g, "") || "0"}${decimalPart.padEnd(2, "0").slice(0, 2)}`;
  const amount = BigInt(cents || "0");

  return negative ? -amount : amount;
}

export function formatCurrency(value: string | bigint): string {
  const minorUnits = typeof value === "bigint" ? value : decimalToMinorUnits(value);
  const negative = minorUnits < 0n;
  const unsigned = negative ? -minorUnits : minorUnits;
  const integerPart = (unsigned / 100n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  const decimalPart = (unsigned % 100n).toString().padStart(2, "0");

  return `${negative ? "-R$" : "R$"} ${integerPart},${decimalPart}`;
}
