import { escapeHtml } from './html.js';

export function memberCard(member) {
  return `<li class="member">${escapeHtml(member.name)}</li>`;
}

export function profilePage(member) {
  return [
    '<article class="profile">',
    `  <h1>${member.name}</h1>`,
    `  <p class="bio">${escapeHtml(member.bio ?? '')}</p>`,
    `  <p class="joined">Member since ${escapeHtml(member.joined)}</p>`,
    '</article>',
  ].join('\n');
}
