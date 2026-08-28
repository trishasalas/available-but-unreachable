-- caption-style-tmlr.lua
-- TMLR variant of caption-style.lua.
--
-- The original filter emits \figurecaptionfont and \color[HTML]{6E6E6E}.
-- \figurecaptionfont is a fontspec \newfontfamily (Atkinson Hyperlegible
-- Italic) defined only in build/template.tex, which requires lualatex. The
-- TMLR build runs pdflatex with Latin Modern, so that macro does not exist
-- and the colored 12pt caption would be off-format anyway.
--
-- This version uses only base LaTeX: \small\itshape, no color, no font switch.
--
-- Converts ::: {.caption} ... ::: divs to a styled caption block.
-- Usage: pandoc --lua-filter=build/filters/caption-style-tmlr.lua

function Div(el)
  if el.classes:includes("caption") then
    local content = pandoc.write(pandoc.Pandoc(el.content), "latex")
    local latex = table.concat({
      "\\vspace{0.25em}",
      "{\\small\\itshape",
      content:gsub("%s+$", ""),  -- trim trailing whitespace
      "\\par}",
      "\\vspace{1em}",
    }, "\n")
    return pandoc.RawBlock("latex", latex)
  end
end
