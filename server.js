/**
 * 프로젝트 루트(doc_load, index.html, CSI API) 서빙
 * 실행: node server.js
 * 브라우저: http://localhost:3840/ (CSI 조회), http://localhost:3840/123-01-06.html (doc_load)
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3840;
const ROOT = __dirname;
const DOC_LOAD = path.join(ROOT, 'doc_load');
const HTTP_LOAD = path.join(ROOT, 'http_load');
const CSI_XLSX = path.join(ROOT, 'CSI.xlsx');

function serveFile(filePath, res) {
    const ext = path.extname(filePath);
    const types = {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css',
        '.js': 'text/javascript',
        '.json': 'application/json; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif',
        '.ico': 'image/x-icon'
    };
    res.setHeader('Content-Type', types[ext] || 'application/octet-stream');
    fs.createReadStream(filePath).pipe(res);
}

function serveApiCsi(res) {
    try {
        const XLSX = require('xlsx');
        const wb = XLSX.readFile(CSI_XLSX);
        const ws = wb.Sheets[wb.SheetNames[0]];
        const data = XLSX.utils.sheet_to_json(ws);
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify(data));
    } catch (e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: String(e.message) }));
    }
}

const server = http.createServer((req, res) => {
    const url = (req.url || '').split('?')[0];

    if (req.method === 'GET' && url === '/api/csi') {
        serveApiCsi(res);
        return;
    }
    if (req.method === 'GET' && (url === '/' || url === '/index.html')) {
        serveFile(path.join(ROOT, 'index.html'), res);
        return;
    }
    if (req.method === 'GET' && url === '/csi.json') {
        const jsonPath = path.join(ROOT, 'csi.json');
        if (fs.existsSync(jsonPath)) {
            serveFile(jsonPath, res);
        } else {
            res.writeHead(404);
            res.end('Not Found');
        }
        return;
    }

    if (req.method === 'POST' && url === '/save') {
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

    // http_load 파일 서빙
    if (req.method === 'GET' && url.startsWith('/http_load/')) {
        const hPath = url.slice('/http_load'.length) || '/';
        const hFile = path.join(HTTP_LOAD, path.normalize(hPath).replace(/^(\.\.(\/|\\|$))+/, ''));
        if (!hFile.startsWith(HTTP_LOAD)) { res.writeHead(403); res.end(); return; }
        fs.stat(hFile, (err, stat) => {
            if (err || !stat.isFile()) { res.writeHead(404); res.end('Not Found'); return; }
            serveFile(hFile, res);
        });
        return;
    }

    let reqPath = url || '/';
    if (reqPath.startsWith('/doc_load/')) reqPath = reqPath.slice('/doc_load'.length) || '/';
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
    console.log('서버: http://localhost:' + PORT + '/');
    console.log('  CSI 조회: http://localhost:' + PORT + '/');
    console.log('  doc_load: http://localhost:' + PORT + '/123-01-06.html');
});
