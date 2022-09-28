
/*
Command line args
Xpath replace char
sink : NULL Pointer Dereference
*/
/*
Created by Paul E. Black and William Mentzer 2020

This software was developed at the National Institute of Standards and Technology
by employees of the Federal Government in the course of their official duties.
Pursuant to title 17 Section 105 of the United States Code the software is not
subject to copyright protection and are in the public domain.

We would appreciate acknowledgment if the software is used.

Paul E. Black  paul.black@nist.gov
William Mentzer willmentzer20@gmail.com

*/
using System;

namespace default_namespace{
    class MainClass63649{
        public static void Main(string[] args){
            
            
            
            
               int num, sum = 0, r;
               System.Console.WriteLine("Hello, World!");
               int[] intArray = new int[7] { 2,37,849,24,42,-10,93 };
               Array.Sort(intArray);
               foreach (int nb in intArray){
                   r = nb + 3;
                   num = r / 10;
                   sum = num + nb;
                   Console.WriteLine("Current sum : "+sum);
               }
               string cmd = null;
               cmd = Environment.GetEnvironmentVariable("cmd");
               //flaw
               cmd = cmd.Trim();
               int a = 0;
               int b = 1;
               for (int i = 0; i < sum; i++){
                   int temp = a;
                   a = b;
                   b = temp + b;
               }
               Console.WriteLine("Fib : "+a);
           
            
        }
        
    }
}
