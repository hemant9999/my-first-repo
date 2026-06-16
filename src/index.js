function hello(name = 'World') {
  return `Hello, ${name}!`;
}

if (require.main === module) {
  console.log(hello());
}

module.exports = { hello };
