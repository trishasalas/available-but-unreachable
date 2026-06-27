-- caption-style.lua
-- Converts ::: {.caption} ... ::: divs to styled LaTeX caption environment.
-- Produces: footnotesize, Atkinson Hyperlegible Mono, #767676 gray, tight top spacing.
--
-- Usage: pandoc --lua-filter=paper/filters/caption-style.lua

function Div(el)
  if el.classes:includes("caption") then
    local content = pandoc.write(pandoc.Pandoc(el.content), "latex")
    local latex = table.concat({
      "\\vspace{0.25em}",
      "{\\fontsize{12pt}{-15pt}\\selectfont\\figurecaptionfont\\color[HTML]{6E6E6E}",
      content:gsub("%s+$", ""),  -- trim trailing whitespace
      "\\par}",
      "\\vspace{1em}",
    }, "\n")
    return pandoc.RawBlock("latex", latex)
  end
end
