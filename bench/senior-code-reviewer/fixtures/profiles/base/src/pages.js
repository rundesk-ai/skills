import { escapeHtml } from './html.js';

export function memberCard(member) {
  return `<li class="member">${escapeHtml(member.name)}</li>`;
}
