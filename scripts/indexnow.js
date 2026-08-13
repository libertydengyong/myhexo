'use strict';

const SITES = [
  {
    host: 'vpsjq.com',
    key: 'vpsjqindexnowkey1786276558',
    keyLocation: 'https://vpsjq.com/vpsjqindexnowkey1786276558.txt'
  }
];

const https = require('https');

function submitIndexNow(site, urlList) {
  if (!urlList.length) return;

  const payload = JSON.stringify({
    host: site.host,
    key: site.key,
    keyLocation: site.keyLocation,
    urlList: urlList
  });

  const options = {
    hostname: 'api.indexnow.org',
    path: '/indexnow',
    method: 'POST',
    timeout: 3000,
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  };

  const req = https.request(options, (res) => {
    console.log(`[IndexNow] ${site.host} -> HTTP ${res.statusCode} (提交了 ${urlList.length} 个URL)`);
    res.resume();
  });

  req.on('timeout', () => {
    console.log(`[IndexNow] ${site.host} 请求超时(3秒)，已放弃，不影响本次生成`);
    req.destroy();
  });

  req.on('error', (err) => {
    console.log(`[IndexNow] ${site.host} 提交失败: ${err.message}`);
  });

  req.write(payload);
  req.end();
}

hexo.extend.filter.register('after_generate', function () {
  const posts = this.locals.get('posts');
  const today = new Date();
  const todayStr = today.toISOString().slice(0, 10);

  const todayUrls = [];
  posts.forEach((post) => {
    const dateStr = post.date ? post.date.format('YYYY-MM-DD') : '';
    const updatedStr = post.updated ? post.updated.format('YYYY-MM-DD') : '';
    if (dateStr === todayStr || updatedStr === todayStr) {
      todayUrls.push(this.config.url.replace(/\/$/, '') + post.path);
    }
  }, this);

  if (todayUrls.length === 0) {
    console.log('[IndexNow] 今天没有新增/更新的文章，跳过提交');
    return;
  }

  SITES.forEach((site) => {
    submitIndexNow(site, todayUrls);
  });
});
