() => {
    // 1. Clica em todas as sanfonas/módulos para abrir a lista de aulas
    const selectors = [
        '.accordion-header',
        '.elementor-accordion-item',
        '.tutor-accordion-item',
        '.ld-item-list-header',
        '[class*="module"]',
        '[class*="section"]',
        '[class*="accordion"]',
        '.toggle-title'
    ];
    
    document.querySelectorAll(selectors.join(',')).forEach(el => {
        try { el.click(); } catch(e) {}
    });

    // 2. Coleta os links e títulos das aulas
    const rawLessons = [];
    const links = Array.from(document.querySelectorAll('a[href*="/cursos/"], a[href*="/aula/"], a[href*="/aulas/"], a[href*="/lesson/"]'));

    links.forEach((a) => {
        const href = a.href;
        const title = a.innerText ? a.innerText.replace(/\n/g, ' ').trim() : a.textContent.trim();
        const ignoredKeywords = ['sair', 'logout', 'meu perfil', 'carrinho', 'minha conta', 'suporte'];
        const isIgnored = ignoredKeywords.some(kw => title.toLowerCase().includes(kw));

        if (href && title && title.length > 1 && !isIgnored) {
            let moduleTitle = "Módulo Único";
            const parentModule = a.closest('[class*="section"], [class*="module"], [class*="accordion"], [class*="topic"], .widget');
            
            if (parentModule) {
                const header = parentModule.querySelector('h1, h2, h3, h4, h5, header, [class*="title"], [class*="header"]');
                if (header) {
                    moduleTitle = header.innerText.replace(/\n/g, ' ').trim();
                }
            }

            rawLessons.push({
                title: title,
                url: href,
                module: moduleTitle
            });
        }
    });

    // 3. Remove duplicatas e ordena as aulas
    const uniqueLessons = [];
    const seenUrls = new Set();
    let index = 1;

    for (const item of rawLessons) {
        if (!seenUrls.has(item.url)) {
            seenUrls.add(item.url);
            item.index = index++;
            uniqueLessons.push(item);
        }
    }

    return uniqueLessons;
}