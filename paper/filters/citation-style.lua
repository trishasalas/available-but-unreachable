function Span(el)
  if not el.classes:includes('citealp') then return end
  return el.content:walk({Cite = function(c)
    if c.content[1] and c.content[1].t == 'Str' then
      c.content[1].text = c.content[1].text:gsub('^%(', '')
    end
    local last = c.content[#c.content]
    if last and last.t == 'Str' then last.text = last.text:gsub('%)$', '') end
    return c
  end})
end
