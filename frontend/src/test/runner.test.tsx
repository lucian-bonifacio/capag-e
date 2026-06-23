import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "../App";

describe("frontend test runner", () => {
  it("executes the Vitest sentinel test", () => {
    expect(true).toBe(true);
  });

  it("renders the minimal governed shell", () => {
    render(<App />);

    expect(screen.getByText("CAPAG Analytics")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Fundacao" })).toBeInTheDocument();
    expect(screen.getByText("Sem dados importados")).toBeInTheDocument();
  });
});
