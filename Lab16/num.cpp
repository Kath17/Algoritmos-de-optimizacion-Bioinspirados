#include <iostream>

using namespace std;

double random(double a, double b)
{
  return ((((double)rand())/((double)RAND_MAX) )*(b-a) + a);
}

int main()
{
  cout<<random(-1,1)<<endl;
  cout<<random(-1,1)<<endl;
  cout<<random(-1,1)<<endl;
  cout<<random(-1,1)<<endl;
  cout<<random(-1,1)<<endl;
  cout<<random(-1,1)<<endl;
  cout<<((((double)rand())/((double)RAND_MAX) )*(1+1) - 1)<<endl;
}
