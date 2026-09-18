-- Keep each image with its existing caption and allow artifact paths to wrap.
function Code(el)
  if el.text:find('/') and not el.text:find('[{}%%\\]') then
    return pandoc.RawInline('latex', '\\nolinkurl{' .. el.text .. '}')
  end
end
function Blocks(blocks)
  local out = pandoc.List()
  local i = 1
  while i <= #blocks do
    local b, next = blocks[i], blocks[i+1]
    if b.t == 'Para' and #b.content == 1 and b.content[1].t == 'Image'
       and next and next.t == 'Div' and next.classes:includes('caption') then
      out:insert(pandoc.RawBlock('latex', '\\par\\noindent\\begin{minipage}{\\linewidth}'))
      out:insert(b)
      out:insert(next)
      out:insert(pandoc.RawBlock('latex', '\\end{minipage}\\par'))
      i = i + 2
    else
      out:insert(b)
      i = i + 1
    end
  end
  return out
end
