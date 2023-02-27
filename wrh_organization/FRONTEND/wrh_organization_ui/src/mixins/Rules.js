export const Rules = {
    computed : {
        rules(){
          var rules = []
          if(this.field ){
            // Required
            if (this.field.required){
              rules.push( v => !!v || this.field.name+' is required')
            }
            // Max Length
            if (this.field.max_length){
              rules.push(v => v && v.length <= parseInt(this.field.max_length) || 'Max '+ this.field.max_length +' characters')


            }
            // Other Rules
            if(this.field.other_rules){
              for(var other_rules of this.field.other_rules){
                if (other_rules == 'SWA'){rules.push(v => (v && /^[A-Za-z]/.test(v)) || 'Need to start with Alphabet')}
                if(other_rules == 'DASC'){rules.push(v => (v && /^[A-Za-z][A-Za-z\d _-]*$/.test(v)) || 'special characters not allowed(except : _ and -)')}
                if(other_rules == 'PNUM'){rules.push(v => (v && !isNaN(parseFloat(v) && parseFloat(v) > 0) || 'Only Positivities are allowed') )}
              }

            }
          } else {
            rules = []
          }
          return rules
        }
      }
}
