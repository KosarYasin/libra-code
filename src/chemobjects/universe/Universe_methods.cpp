#include "Universe.h"

namespace libchemobjects{
namespace libuniverse{


void Universe::Add_Element_To_Periodic_Table(Element rec){
/*********************************************************************
   This is user-interface function. It checks for existance of the
   Element rec in array PeriodicTable. If this element  exists
   - do nothing if it does not - add it to array
   Returns 1 if this is a new record (it just has been added) and 0 if
   record existed in array (we did not add it this time). Returns -1
   if there is an error.
*********************************************************************/
  int res = 1;
  map<std::string,Element>::iterator it;
  if(rec.is_Elt_name){
    it = PeriodicTable.find(rec.Elt_name);
    if(it!=PeriodicTable.end()){
    // Element has been succesfully found
    // That means the element already exist
    res = 0;
    }
  }
  else{
    std::cout<<"To add element record to the Periodic Table its Elt_name property should be defined"<<std::endl;
    res = -1;
  }
  if(res==1){
    // We will add this element to the Periodic Table
    PeriodicTable[rec.Elt_name] = rec;
  }
  else if(res==0){
    // In this case we need to merge rec with existing atom record
  }
}


Element Universe::Get_Element(std::string elt){
 int res = 0;
 Element el;
  // Very first step - check for periodic system!
  if(PeriodicTable.size()>0){
  }else{
    std::cout<<"Error:There is no any periodic system of elements defined in Universe"<<std::endl;
    std::cout<<"      First you shoud load properties of elements to existing Universe"<<std::endl;
    exit(10);
  }

  map<std::string,Element>::iterator it;
  it = PeriodicTable.find(elt);
  if(it!=PeriodicTable.end()){   res = 1;  }
  else{  res = 0;
    std::cout<<"Can not find element "<<elt<<" in periodic system defined in this Universe"<<std::endl;
    exit(11);
  }

  if(res){
    el = (*it).second; // Copy element properties
  }
  return el;
}


}// namespace libuniverse
}// namespace libchemobjects
