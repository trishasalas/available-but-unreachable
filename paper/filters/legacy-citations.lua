-- Preserve the manuscript's existing natbib author-year citations with citeproc.
function RawInline(el)
  if el.format ~= "tex" and el.format ~= "latex" then return end
  local keys = el.text:match("^\\citealp{([^}]+)}$")
  if not keys then return end
  local citations = {}
  for key in keys:gmatch("[^,%s]+") do
    table.insert(citations, pandoc.Citation(key, "NormalCitation"))
  end
  -- citealp omits parentheses: suppress citeproc's outer parentheses only.
  return pandoc.Span({pandoc.Cite({}, citations)}, {class="citealp"})
end
