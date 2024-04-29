// first java
console.log('Hello world');

// Creating a changable variable
let name = 'Mosh';

// Creating a constant variable
const interestRate = 0.3;
console.log(interestRate);

//Primitives/Values: strings, int, bolean, undefined and null 
let name1 = 'Pan'
let age = 30
let isApproved = false;
let firstName = undefined; //or let firstName;
let LastName = null;

//Reference: object, array, function
let person = {
   name: 'Mosh', 
   age: 30,
};

//Dot notation
person.name = 'John';
//Bracket notation (can change dynamically)
let selection = 'name';
person[selection] = 'Mary';

console.log(person.name);

//Arrays
let selectedColors = ['red', 'blue'];
selectedColors[2] = 4;
console.log(selectedColors);

//Functions
function greet(name) {
   console.log('hello' + name);
}
greet('John');
