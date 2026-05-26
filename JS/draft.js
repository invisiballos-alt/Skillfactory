const firstFunction = (num) => {
  console.log(`Первая функция работает, аргумент равен ${num}`);
};

const secondFunction = (a) => {
  console.log("Вторая функция работает");
  return firstFunction(a);
};

const thirdFunction = () => {
  console.log("Третья функция работает");
  return secondFunction(3);
};

thirdFunction();
