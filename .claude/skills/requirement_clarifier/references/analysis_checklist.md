# Requirement Clarification Analysis Checklist

## 1️⃣ Ambiguity Detection Checklist

### Common Ambiguity Patterns
- [ ] **Vague Terms**: Look for words like "soon", "fast", "efficient", "user-friendly"
- [ ] **Undefined Acronyms**: Ensure all acronyms are defined
- [ ] **Unclear Pronouns**: Identify "it", "this", "that" without clear references
- [ ] **Relative Terms**: Find "large", "small", "many", "few" without quantification
- [ ] **Assumed Knowledge**: Identify domain knowledge assumed but not stated
- [ ] **Context Dependency**: Check for requirements that depend on unstated context

### Language Analysis
- [ ] **Multiple Meanings**: Words that could be interpreted in different ways
- [ ] **Subjective Terms**: Requirements based on personal opinion or preference
- [ ] **Incomplete Sentences**: Missing subjects, objects, or predicates
- [ ] **Conditional Ambiguity**: "if" statements without clear conditions

## 2️⃣ Missing Constraints Checklist

### Performance Constraints
- [ ] **Response Time**: Maximum acceptable response times
- [ ] **Throughput**: Required processing capacity
- [ ] **Resource Usage**: Memory, CPU, storage limitations
- [ ] **Concurrency**: Number of simultaneous users/operations

### Operational Constraints
- [ ] **Availability**: Required uptime percentages
- [ ] **Reliability**: Expected failure rates
- [ ] **Maintainability**: Update and maintenance requirements
- [ ] **Scalability**: Growth capacity requirements

### Technical Constraints
- [ ] **Platform Requirements**: OS, browser, device compatibility
- [ ] **Integration**: Required connections to other systems
- [ ] **Standards Compliance**: Industry or regulatory standards
- [ ] **Security**: Authentication, authorization, encryption needs

## 3️⃣ Unstated Assumptions Checklist

### User Assumptions
- [ ] **Skill Level**: Expected user technical expertise
- [ ] **Frequency of Use**: How often users will interact
- [ ] **Environment**: Where and how the system will be used
- [ ] **Training**: Whether users will receive training

### Business Assumptions
- [ ] **Data Sources**: Where data will come from
- [ ] **Business Rules**: Unstated company policies or procedures
- [ ] **Regulatory Compliance**: Legal or regulatory requirements
- [ ] **Budget Constraints**: Financial limitations not stated

### Technical Assumptions
- [ ] **Infrastructure**: Available hardware or software
- [ ] **External Dependencies**: Third-party services or APIs
- [ ] **Development Timeline**: Project schedule expectations
- [ ] **Team Expertise**: Available technical skills

## 4️⃣ Edge Case Analysis Checklist

### Input Boundaries
- [ ] **Minimum Values**: Lowest acceptable inputs
- [ ] **Maximum Values**: Highest acceptable inputs
- [ ] **Zero Values**: Behavior with null/empty inputs
- [ ] **Negative Values**: Handling of negative numbers
- [ ] **Special Characters**: Unicode, symbols, formatting characters

### State Transitions
- [ ] **Initial State**: System behavior at startup
- [ ] **Error States**: Recovery from various error conditions
- [ ] **Concurrent Access**: Multiple users accessing simultaneously
- [ ] **Interrupted Operations**: Handling of incomplete operations

### Environmental Factors
- [ ] **Network Issues**: Behavior during connectivity problems
- [ ] **Resource Constraints**: Behavior with limited memory/disk
- [ ] **Time Zones**: Handling of different time zones
- [ ] **Localization**: Language and cultural differences

## 5️⃣ Critical Clarification Questions

### Scope Questions
- [ ] What exactly needs to be built vs. what is out of scope?
- [ ] Who is the target user and what are their needs?
- [ ] What are the non-functional requirements?
- [ ] What are the success criteria for the project?

### Technical Questions
- [ ] What technologies are required or prohibited?
- [ ] What existing systems need integration?
- [ ] What are the performance and scalability requirements?
- [ ] What are the security and compliance needs?

### Business Questions
- [ ] What is the timeline and budget?
- [ ] What are the business objectives?
- [ ] Who are the stakeholders and decision makers?
- [ ] What are the risk tolerance levels?

### Operational Questions
- [ ] How will the system be maintained and updated?
- [ ] What kind of support is needed?
- [ ] How will success be measured?
- [ ] What happens if the system fails?

## 6️⃣ Quality Validation Checklist

### Completeness Check
- [ ] All functional requirements are specified
- [ ] All non-functional requirements are included
- [ ] All constraints are documented
- [ ] All interfaces are defined

### Consistency Check
- [ ] Requirements don't contradict each other
- [ ] Terminology is used consistently
- [ ] Standards and formats are uniform
- [ ] Assumptions are consistent across requirements

### Verifiability Check
- [ ] Each requirement can be tested
- [ ] Success criteria are measurable
- [ ] Acceptance criteria are clear
- [ ] Test scenarios can be defined

### Feasibility Check
- [ ] Requirements are technically achievable
- [ ] Requirements fit within constraints
- [ ] Requirements align with business goals
- [ ] Requirements are cost-effective to implement