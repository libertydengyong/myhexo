hexo.extend.filter.register('before_post_render', function (data) {
  const moreTag = '<!-- more -->';

  // 如果文章里没有 more，就自动插入
  if (!data.content.includes(moreTag)) {
    const paragraphs = data.content.split('\n');

    if (paragraphs.length > 1) {
      data.content =
        paragraphs[0] +
        '\n\n' +
        moreTag +
        '\n\n' +
        paragraphs.slice(1).join('\n');
    }
  }

  return data;
});

