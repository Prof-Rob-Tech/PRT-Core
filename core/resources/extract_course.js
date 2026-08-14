(() => {
    const lessons = [];
    const seen = new Set();
    
    // Procura por todos os links que contêm '/aula/'
    const links = Array.from(document.querySelectorAll('a[href*="/aula/"]'));
    
    links.forEach((link, index) => {
        const href = link.href;
        if (!href || seen.has(href)) return;
        seen.add(href);
        
        // Extrai o título da aula
        let title = link.innerText.trim() || `Aula ${index + 1}`;
        title = title.replace(/\s+/g, ' ');
        
        // Tenta descobrir o nome do módulo pai
        let moduleName = "Módulo Único";
        const parentModule = link.closest('.elementor-accordion-item, .tutor-accordion-item, .accordion-item, .module, .tutor-course-topic');
        
        if (parentModule) {
            const header = parentModule.querySelector('.elementor-accordion-title, .tutor-accordion-item-header, h2, h3, h4, .title');
            if (header) {
                moduleName = header.innerText.trim().replace(/\s+/g, ' ');
            }
        }
        
        lessons.push({
            url: href,
            title: title,
            module: moduleName,
            index: index + 1
        });
    });
    
    return lessons;
})();