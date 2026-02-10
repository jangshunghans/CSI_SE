/**
 * doc_load 폴더를 서빙하고, 저장 요청 시 doc_load에 직접 저장 (다운로드 창 없음)
 * 실행: node server.js
 * 브라우저: http://localhost:3840/123-01-06.html
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3840;
const DOC_LOAD = path.join(__dirname, 'doc_load');

function serveFile(filePath, res) {
    const ext = path.extname(filePath);
    const types = {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css',
        '.js': 'text/javascript',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif',
        '.ico': 'image/x-icon'
    };
    res.setHeader('Content-Type', types[ext] || 'application/octet-stream');
    fs.createReadStream(filePath).pipe(res);
}

const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/save') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
            try {
                const { filename, content } = JSON.parse(body);
                if (!filename || !content) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ ok: false, error: 'filename and content required' }));
                    return;
                }
                const base = path.basename(filename);
                if (base !== filename || base.indexOf('..') !== -1) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ ok: false, error: 'invalid filename' }));
                    return;
                }
                const filePath = path.join(DOC_LOAD, base);
                fs.writeFileSync(filePath, content, 'utf8');
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ ok: true }));
            } catch (e) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ ok: false, error: String(e.message) }));
            }
        });
        return;
    }

    const reqPath = (req.url === '/' || req.url === '') ? '/123-01-06.html' : req.url;
    const filePath = path.join(DOC_LOAD, path.normalize(reqPath).replace(/^(\.\.(\/|\\|$))+/, ''));
    if (!filePath.startsWith(DOC_LOAD)) {
        res.writeHead(403);
        res.end();
        return;
    }
    fs.stat(filePath, (err, stat) => {
        if (err || !stat.isFile()) {
            res.writeHead(404);
            res.end('Not Found');
            return;
        }
        serveFile(filePath, res);
    });
});

server.listen(PORT, () => {
    console.log('doc_load 서버: http://localhost:' + PORT + '/');
    console.log('예: http://localhost:' + PORT + '/123-01-06.html');
});
