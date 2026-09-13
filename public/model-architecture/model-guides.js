function controllerSection(model) {
  const c = model.controller;
  if (!c) return '';
  const rows = [['适用本体', c.platform], ['模型 → 控制器', c.interface], ['控制器的职责', c.execution], ['接入 G1 / SONIC', c.adaptation]];
  return '<section class="section controller-section" aria-label="WBC 与执行接口">' +
    '<div class="kicker">CONTROL · WBC 与执行接口</div>' +
    '<h3 class="controller-intro">' + esc(c.name) + '</h3>' +
    '<p class="controller-status">' + esc(c.status) + '</p>' +
    '<dl class="controller-table">' + rows.map(([label, value]) => '<div><dt>' + esc(label) + '</dt><dd>' + esc(value) + '</dd></div>').join('') + '</dl>' +
    '<div class="sources">' + c.sources.map(s => '<a target="_blank" rel="noopener noreferrer" href="' + esc(s.url) + '">' + esc(s.label) + ' ↗</a>').join('') + '</div>' +
    '<p class="controller-checked">接口资料核对：' + esc(c.checkedAt) + '</p>' +
    (model.availability ? '<p class="availability-note">' + esc(model.availability) + '</p>' : '') + '</section>';
}

function modelFigures(model) {
  const groups = model.figureGroups || [];
  if (!groups.length) return '';
  const figure = (item, deferred) => '<figure class="model-figure">' +
    '<a href="' + esc(item.src) + '" target="_blank" rel="noopener" aria-label="打开大图：' + esc(item.alt) + '">' +
    '<img ' + (deferred ? 'data-src' : 'src') + '="' + esc(item.src) + '" alt="' + esc(item.alt) + '" width="' + item.width + '" height="' + item.height + '" loading="lazy" decoding="async"></a>' +
    '<figcaption><span>' + esc(item.caption) + '<small>' + Math.round(item.bytes / 1024) + ' KB · WebP</small></span>' +
    '<a href="' + esc(item.src) + '" target="_blank" rel="noopener">打开完整大图 ↗</a></figcaption></figure>';
  const groupContent = group => '<p class="model-figure-source">' + (group.sourceUrl ? '<a href="' + esc(group.sourceUrl) + '">' + esc(group.source) + '</a>' : esc(group.source)) + '</p>' + group.images.map(item => figure(item, !!group.collapsed)).join('');
  const notes = model.figureNotes?.length ? '<aside class="model-figure-notes"><h4>读图说明 · 结合正文与官方实现</h4><ul>' + model.figureNotes.map(note => '<li>' + esc(note) + '</li>').join('') + '</ul></aside>' : '';
  return '<section class="section model-figures" aria-label="架构图解"><div class="kicker">ILLUSTRATED GUIDE · 架构图解</div><h3>架构总览与内部模块详解</h3>' + notes +
    groups.map(group => group.collapsed ? '<details class="model-figure-extra"><summary>' + esc(group.title) + '</summary>' + groupContent(group) + '</details>' : '<div class="model-figure-group"><h4>' + esc(group.title) + '</h4>' + groupContent(group) + '</div>').join('') + '</section>';
}

function prepareModelFigures() {
  document.querySelectorAll('#detail .model-figure-extra').forEach(group => {
    group.addEventListener('toggle', () => {
      if (!group.open) return;
      group.querySelectorAll('img[data-src]').forEach(img => {
        img.src = img.dataset.src;
        delete img.dataset.src;
      });
    });
  });
}
