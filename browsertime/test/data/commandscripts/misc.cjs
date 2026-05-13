module.exports = async function (context, commands) {
  await commands.navigate('http://127.0.0.1:3000/search/');
  await commands.addText('id:search-input', 'grafana');
  await commands.set('id:search-input', 'grafana2', 'innerText');
  await commands.set('#search-input', 'grafana3', 'innerText');
  await commands.wait.byTime(500);
  await commands.js.run('document.body.style.backgroundColor="red"');
  await commands.measure.start('http://127.0.0.1:3000/simple/');
  await commands.navigation.back({ waitForNavigation: true });
  await commands.navigation.forward({ waitForNavigation: true });
  await commands.navigation.refresh({ waitForNavigation: true });

  await commands.switch.toNewTab('http://127.0.0.1:3000/simple/');
  return commands.switch.toNewWindow('http://127.0.0.1:3000/dimple/');
};
