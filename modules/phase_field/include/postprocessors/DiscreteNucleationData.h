//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html

#ifndef DISCRETENUCLEATIONDATA_H
#define DISCRETENUCLEATIONDATA_H

#include "GeneralPostprocessor.h"
#include "DiscreteNucleationInserter.h"

class DiscreteNucleationData;

template <>
InputParameters validParams<DiscreteNucleationData>();

/**
 * Output diagnostic data on a DiscreteNucleationInserter
 */
class DiscreteNucleationData : public GeneralPostprocessor
{
public:
  DiscreteNucleationData(const InputParameters & parameters);

  void execute() override{};
  void initialize() override{};

  Real getValue() override;

protected:
  /// UserObject that manages nucleus insertin and deletion
  const DiscreteNucleationInserter & _inserter;

  /// list of nuclei maintained bu the inserter object
  const DiscreteNucleationInserter::NucleusList & _nucleus_list;

  /// Type of value to report back
  enum class ValueType
  {
    COUNT,
    UPDATE
  } _value_type;
};

#endif // DISCRETENUCLEATIONDATA_H