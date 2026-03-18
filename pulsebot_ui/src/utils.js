export function generateSessionId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
  });
}

export function escapeHtml(text) {
  if (!text) return '';
  return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
}

export function formatMessage(text) {
  if (!text) return '';

  // Escape HTML first
  text = escapeHtml(text);

  // Store code blocks to protect from other transformations
  const codeBlocks = [];
  text = text.replace(/```(\w*)\n?([\s\S]*?)```/g, (match, lang, code) => {
      codeBlocks.push(`<pre><code>${code.trim()}</code></pre>`);
      return `%%CODEBLOCK${codeBlocks.length - 1}%%`;
  });

  // Inline code (protect from other transformations)
  const inlineCodes = [];
  text = text.replace(/`([^`]+)`/g, (match, code) => {
      inlineCodes.push(`<code>${code}</code>`);
      return `%%INLINECODE${inlineCodes.length - 1}%%`;
  });

  // Process tables
  text = text.replace(/(?:^|\n)(\|.+\|)\n(\|[-:| ]+\|)\n((?:\|.+\|\n?)+)/g, (match, header, separator, body) => {
      const headerCells = header.split('|').filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join('');
      const rows = body.trim().split('\n').map(row => {
          const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
          return `<tr>${cells}</tr>`;
      }).join('');
      return `\n<table><thead><tr>${headerCells}</tr></thead><tbody>${rows}</tbody></table>\n`;
  });

  // Headers (must be at start of line)
  text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // Horizontal rules
  text = text.replace(/^---+$/gm, '<hr>');

  // Unordered lists
  text = text.replace(/(?:^|\n)((?:[-*] .+\n?)+)/g, (match, list) => {
      const items = list.trim().split('\n').map(item => {
          const content = item.replace(/^[-*] /, '');
          return `<li>${content}</li>`;
      }).join('');
      return `\n<ul>${items}</ul>\n`;
  });

  // Ordered lists
  text = text.replace(/(?:^|\n)((?:\d+\. .+\n?)+)/g, (match, list) => {
      const items = list.trim().split('\n').map(item => {
          const content = item.replace(/^\d+\. /, '');
          return `<li>${content}</li>`;
      }).join('');
      return `\n<ol>${items}</ol>\n`;
  });

  // Bold
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Italic
  text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Restore inline codes
  inlineCodes.forEach((code, i) => {
      text = text.replace(`%%INLINECODE${i}%%`, code);
  });

  // Restore code blocks
  codeBlocks.forEach((block, i) => {
      text = text.replace(`%%CODEBLOCK${i}%%`, block);
  });

  // Convert remaining newlines to <br> (but not around block elements)
  text = text.replace(/\n(?!<\/?(?:table|thead|tbody|tr|th|td|ul|ol|li|h[1-3]|hr|pre))/g, '<br>');

  // Clean up extra line breaks around block elements
  text = text.replace(/<br>\s*(<(?:table|ul|ol|h[1-3]|hr|pre))/g, '$1');
  text = text.replace(/(<\/(?:table|ul|ol|h[1-3]|hr|pre)>)\s*<br>/g, '$1');

  return text;
}
