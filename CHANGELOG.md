## 20260820

- 📦 新增符合当前 Codex 规范的 skills-only 插件清单 `.codex-plugin/plugin.json`
- 🧩 新增 GitHub repo marketplace，可从 Codex 桌面端添加并安装
- 🗂️ 将 Skill、脚本、模板和 Lua 过滤器整理为自包含插件目录
- ✅ 新增纯标准库的本地插件结构校验，不依赖 GitHub Actions
- 📝 更新远程安装说明与 Pandoc 外部依赖边界


## 20260517

- 🎨 新增Skill.md，支持Agent调用
- 📝 模板体积减小


## 20260122

- 🎨 lua为段落的单个图片添加Figure样式，word模板添加Figure居中样式
- 🎨 行内代码与代码块分离，添加lua脚本和word样式
- 📝支持在任意位置调用`markdown-to-docx.lua`

## 20260119
- 完善模板
- 完善README
- 添加`preserve_font_color.lua`，实现字体颜色保留

## 20251217
- 添加Markdown和word互转脚本
- 添加`templates_sci论文模板_标题不编号.docx`
- README添加博客链接

## 20250905
- 新增`markdown-html-recognition.lua`，解决pandoc不支持解析markdown中的html标签的问题，比如`<sub>`、`<sup>`、`<img>`·等
- 新增`markdown-to-docx.lua`，统一调用`markdown-html-recognition.lua`和`image-title-to-caption.lua`

## 2025.07.25

- 新增image-title-to-caption-add-number.lua，对图片标题进行编号

## 2025.06.05

- 💄 style(样式): compact样式由居中改为居左，因为md转docx的列表样式会包含compact（html貌似不会）
- ✨ 添加image-title-to-caption.lua，pandoc默认的图片标题是alt文本，如果要修改图片标题为title文本而不是alt文本，可以用该lua脚本
    ```bash
    pandoc --reference-doc template.docx -s input.md  -o output.docx --lua-filter image-title-to-caption.lua
    ```
    相关博客：https://www.achuan-2.top/post/pandoc-exports-markdown-as-docx-how-to-modify-image-title-to-title-text-instead-of-alt-text-19kkpr.html

## 2024.12.03

- ✨ 改进代码块样式：代码块左缩进三个字符，字体为五号字体，这样与普通段落更对齐
    
    ![](https://fastly.jsdelivr.net/gh/Achuan-2/PicBed/assets/PixPin_2024-12-03_21-30-13-2024-12-03.png)

## 2024.12.02

- ✨ 改进引述块样式：美化样式，去除首行缩进，添加左缩进，与前一个段落的首行对齐

    ![](https://fastly.jsdelivr.net/gh/Achuan-2/PicBed/assets/PixPin_2024-12-02_15-27-00-2024-12-02.png)

## 2024.02.03 
- zotero 参考文献格式优化，zotero文献引用用的是【书目】样式，设置小四号中文宋体，悬挂缩进2字符

## 2024.01.15
- 🐛 页边距设置为常规
- ✨ 修改blockquote导出样式，设置文本块后续样式依然是文本块
    ![1705302906882Snipaste_2024-01-15_15-15-04.png](https://fastly.jsdelivr.net/gh/Achuan-2/PicBed@pic/assets/1705302906882Snipaste_2024-01-15_15-15-04.png)
- ✨ 添加有序列表设置右对齐，这样编号1和11可以对齐（不顶格模板暂时没设置）
    ![1705300595618Snipaste_2024-01-15_14-36-29.png](https://fastly.jsdelivr.net/gh/Achuan-2/PicBed@pic/assets/1705300595618Snipaste_2024-01-15_14-36-29.png)
- ✨ 添加列表第二行顶格模板
    列表第二行不顶格
    ![1705299592624Snipaste_2024-01-15_14-19-46.png](https://fastly.jsdelivr.net/gh/Achuan-2/PicBed@pic/assets/1705299592624Snipaste_2024-01-15_14-19-46.png)
    列表第二行顶格效果
    ![1705299404618Snipaste_2024-01-15_14-16-34.png](https://fastly.jsdelivr.net/gh/Achuan-2/PicBed@pic/assets/1705299404618Snipaste_2024-01-15_14-16-34.png)

## 2023.12.20
- ✨ 页面大小设置为A4

## 2023.12.20
-  🎉 初次提交
