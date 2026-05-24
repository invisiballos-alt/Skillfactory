function SortedNumbers(arr) {
    const uniqueArray = [...new Set(arr)];
    
    return uniqueArray.sort((a, b) => a - b);
}

const numbers = [10, 3, 5, 3, 10, 1, 5, 8];
const result = SortedNumbers(numbers);

console.log(result); 
