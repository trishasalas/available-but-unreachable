-- figure-alt.lua
-- Wraps \includegraphics in explicit tagpdf structure tags for PDF/UA-2 compliance.
-- Uses \tagstructbegin{tag=Figure,alt={...}} which is confirmed working in
-- TeX Live 2025 / tagpdf 0.99+.
--
-- Usage: pandoc --lua-filter=paper/filters/figure-alt.lua

function Image(el)
  local alt = el.attributes["fig-alt"] or ""
  local path = el.src

  -- Escape characters that would break LaTeX argument parsing
  local escaped_alt = alt:gsub("\\", "\\textbackslash ")
                          :gsub("{",  "\\{")
                          :gsub("}",  "\\}")
                          :gsub("%%", "\\%%")

  local latex = table.concat({
    "\\tagstructbegin{tag=Figure,alt={" .. escaped_alt .. "}}",
    "\\tagmcbegin{tag=Figure}",
    "\\includegraphics[width=\\linewidth]{" .. path .. "}",
    "\\tagmcend",
    "\\tagstructend",
  }, "\n")

  return pandoc.RawInline("latex", latex)
end
