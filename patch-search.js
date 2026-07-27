'use strict';

const fs = require('fs');
const path = require('path');

const targetFile = path.join(
  __dirname,
  'node_modules',
  'hexo-generator-searchdb',
  'dist',
  'search.js'
);

if (!fs.existsSync(targetFile)) {
  console.log('[patch-search] 目标文件不存在，跳过（可能还没装hexo-generator-searchdb）');
  process.exit(0);
}

let content = fs.readFileSync(targetFile, 'utf8');

const targetLine = "url.searchParams.append('highlight', keywords.join(' '));";

if (!content.includes(targetLine)) {
  console.log('[patch-search] 未找到目标行，可能已经打过补丁，或者包版本变了，跳过');
  process.exit(0);
}

content = content.replace(
  targetLine,
  '/* [patched by patch-search.js] ' + targetLine + ' */'
);

fs.writeFileSync(targetFile, content, 'utf8');
console.log('[patch-search] 已成功去除搜索结果链接的 highlight 参数拼接');
