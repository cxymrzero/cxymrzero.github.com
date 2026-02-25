# cxymrzero.github.com

这是一个基于 Jekyll 的 GitHub Pages 博客。为复刻 Octopress 的“写完 Markdown 即可生成完整页面”的体验，提供了辅助脚本来自动生成分类页并构建站点。

## 快速开始

安装依赖（仅首次或 Gemfile 更新后需要）：
```bash
bundle install
```

本地预览（自动生成分类页并启动服务）：
```bash
./scripts/generate_all.sh serve
```

构建站点（自动生成分类页并输出到 `_site`）：
```bash
./scripts/generate_all.sh
```

## 自动生成分类页

Jekyll 默认不会为分类自动生成页面。项目提供脚本在每次构建前生成分类页：
```bash
python3 ./scripts/generate_categories.py
```

分类页会生成在：
```
blog/categories/<category>/index.html
```

## 写作流程

1. 在 `_posts/` 新建 Markdown 文件（文件名格式：`YYYY-MM-DD-title.md`）。
2. 确保 front matter 中包含 `categories`（例如 `categories: ["reading"]`）。
3. 运行：
   ```bash
   ./scripts/generate_all.sh serve
   ```

## 发布到 GitHub Pages

这是用户站点仓库（`<username>.github.io` 或 `<username>.github.com`）：
1. `git add -A`
2. `git commit -m "Update blog"`
3. `git push origin main`（如果默认分支是 `master`，改成 `master`）

GitHub Pages 会自动构建并发布。
